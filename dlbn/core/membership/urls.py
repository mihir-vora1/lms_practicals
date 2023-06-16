from django.urls import path
from .views import PlanListView, PlanCheckoutView, payment_confirmation_view, payment_failure_view, stripe_webhook, is_active_plan



urlpatterns = [

    path("plan", PlanListView.as_view(), name="plan-list"),
    path('plans/', PlanListView.as_view(), name='plan-list'),
    path('payment-confirmation/', payment_confirmation_view, name='payment-confirmation'),
    path('payment-failure/', payment_failure_view, name='payment-failure'),
    path('plans/<int:plan_id>/checkout/', PlanCheckoutView.as_view(), name='plan-checkout'),    
    path("webhooks/", stripe_webhook, name="webhooks"),

]
