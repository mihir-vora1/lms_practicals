import stripe
import datetime
import pytz
from django.conf import settings
from .models import Restrict, Plan, Subscription
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from stripe.error import CardError
from django.http import JsonResponse
from django.http import HttpResponse
from stripe.error import SignatureVerificationError
from stripe.error import StripeError


stripe.api_key = settings.STRIPE_SECRET_KEY

class PlanListView(ListView):
    model = Plan
    template_name = "membership/plan.html"
    context_object_name = "plans"

class PlanCheckoutView(View):

    def has_active_subscription(self, user):
        return Subscription.objects.filter(user=user, status='active').exists()

    def get(self, request, *args, **kwargs):

        # if self.has_active_subscription(request.user):
        #     active_subscription = Subscription.objects.get(user=request.user, status='active')
        #     due_date = active_subscription.expire_at
        #     plan_name = active_subscription.plan
        #
        #     return render(request, 'membership/subscription_exists.html', {
        #         'message': f"You already have an active subscription for plan '{plan_name}' with a due date of {due_date}."
        #     })


        plan_id = self.kwargs['plan_id']
        plan = self.get_plan(plan_id)

        request.user.plan = plan
        request.user.save()

        setup_intent = self.generate_setup_intent()

        context = self.get_context(plan, setup_intent)
        return render(request, 'membership/payment.html', context)

    def post(self, request, *args, **kwargs):
        payment_method_id = request.POST.get('payment_method_id')
        setup_intent_id = request.POST.get('setup_intent_id')
        plan_id = self.kwargs['plan_id']
        plan = self.get_plan(plan_id)
        user = request.user
        customer_id = self.get_or_create_customer(payment_method_id, user)

        expiration_date = self.calculate_expiration_date(plan)

        payment_method = self.retrieve_payment_method(payment_method_id)
        try:
            self.attached_payment_method = self.attach_payment_method_to_customer(customer_id, payment_method_id )
        except CardError as e:
            # Handle the card error here
            error_msg = e.user_message if e.user_message else 'Your card was declined.'
            return redirect('payment-failure')
        price_data = stripe.Price.retrieve(plan.price_id)
        if price_data.type == 'one_time':
            return self.process_one_time_payment(plan, self.attached_payment_method.id, customer_id)
        else:
            return self.process_subscription(plan, customer_id, self.attached_payment_method.id, expiration_date, request)


    def attach_payment_method_to_customer(self, customer_id, payment_method_id):
        payment_method = stripe.PaymentMethod.attach(payment_method_id, customer=customer_id)
        return payment_method

    def get_plan(self, plan_id):
        try:
            return Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return redirect('plan-list')

    def generate_setup_intent(self):
        return stripe.SetupIntent.create(payment_method_types=['card'])

    def get_context(self, plan, setup_intent):
        return {
            'plan': plan,
            'client_secret': setup_intent.client_secret,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'intent_id': setup_intent.id
        }

    def get_or_create_customer(self, payment_method_id, user):
        customers = stripe.Customer.list(email=user.email)
        if len(customers) != 0:
            return customers.data[0].get('id')
        else:
            customer = stripe.Customer.create(
                name=user.username,
                email=user.email,
                description=f"Customer for {user.email}",
                payment_method=payment_method_id,
                invoice_settings={'default_payment_method': payment_method_id}
            )
            customer.email = user.email
            customer.name = user.username
            customer.save()
            return customer.id

    def calculate_expiration_date(self, plan):
        expiration_date = None
        if plan.recurring_freq == 'monthly':
            expiration_date = datetime.datetime.now(pytz.UTC) + relativedelta(months=1)
        elif plan.recurring_freq == 'yearly':
            expiration_date = datetime.datetime.now(pytz.UTC) + relativedelta(years=1)
        return expiration_date

    def retrieve_payment_method(self, payment_method_id):
        return stripe.PaymentMethod.retrieve(payment_method_id)

    def process_one_time_payment(self, plan, payment_method_id, customer_id):
        try:
            # Create a one-time payment using PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(plan.price) * 100,
                currency="inr",
                payment_method=payment_method_id,
                customer=customer_id,
                confirm=True,
                off_session=True,
            )

            if payment_intent.status == 'succeeded':
                return redirect('payment-confirmation')
            else:
                return redirect('payment-failure')
        except CardError as e:
            # Handle the card error here
            error_msg = e.user_message if e.user_message else 'Your card was declined.'
            return redirect('payment-failure')

    def process_subscription(self, plan, customer_id, payment_method_id, expiration_date, request):

        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': plan.price_id}],
                expand=['latest_invoice.payment_intent'],
            )

            payment_intent_id = subscription.latest_invoice.payment_intent

            payment_intent = stripe.PaymentIntent.create(
                amount=int(plan.price) * 100,
                currency='inr',
                customer=customer_id,
                payment_method=payment_method_id,
                off_session=True,
                confirm=True,
                receipt_email=request.user.email
            )

            if payment_intent.status == 'succeeded':
                subscription_obj = Subscription.objects.create(
                    user_id=request.user.id,  # Retrieve user from request object
                    plan=plan,
                    customer_id=customer_id,
                    payment_id=payment_intent_id.id,
                    status='active',
                    expire_at=expiration_date if plan.is_recurring else None
                )

                invoice_link = stripe.Invoice.retrieve(subscription.latest_invoice.id).hosted_invoice_url
                return redirect(invoice_link)

            else:
                return redirect('payment-failure')
        except CardError as e:
            # Handle the card error here
            error_msg = e.user_message if e.user_message else 'Your card was declined.'
            return redirect('payment-failure')


def payment_confirmation_view(request):
    messages.success(request, 'Payment succeeded. Thank you for your purchase.')
    return render(request, 'membership/payment_confirmation.html')

def payment_failure_view(request):
    messages.error(request, 'Payment failed. Please try again.')
    return render(request, 'membership/payment_failure.html')

def is_active_plan(request):
    messages.success(request, 'Plan is Already active')
    return render(request, 'membership/is_active_plan.html')


@csrf_exempt
def stripe_webhook(request):
    breakpoint()
    payload = request.body
    sig_header = request.headers['Stripe-Signature']
    endpoint_secret = settings.STRIPE_SECRET_KEY
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        if event['type'] == 'payment_intent.failed':
            payment_intent = event['data']['object']
            error_message = payment_intent.get('last_payment_error', {}).get('message')

            if error_message and 'Your card was declined' in error_message:
                return HttpResponse('Payment failed: Your card was declined.', status=200)

    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    return HttpResponse(status=200)