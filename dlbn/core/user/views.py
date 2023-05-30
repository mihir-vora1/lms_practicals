from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm, ProfileUpdateForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import  LoginSerializer, FollowSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import generics
from .models import Follow, User
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .tasks import send_verification_email
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.http import HttpResponse


from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Generate verification token
            token = default_token_generator.make_token(user)

            # Generate verification link
            current_site = get_current_site(request)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = reverse('verify_email', kwargs={'uidb64': uidb64, 'token': token})
            verification_link = f'{current_site.domain}{verification_link}'

            # Send verification email asynchronously
            send_verification_email.delay(user.email, verification_link)

            # Resend verification link
            resend_verification_link = reverse('resend_verification')

            # The signal will be triggered automatically
            return render(request, "user/success.html", {'resend_verification_link': resend_verification_link})
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.email_verified and user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, 'Your account needs to be verified before you can log in.')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        # Check if token is valid
        if not default_token_generator.check_token(user, token):
            raise ValidationError('Invalid verification link.')

        # Check if the link has expired (e.g., set expiration time to 5 minutes)
        expiration_time = timezone.now() - timezone.timedelta(minutes=5)
        if user.date_joined < expiration_time:
            raise ValidationError('Verification link has expired.')

        user.email_verified = True
        user.is_active = True
        user.save()
        return render(request, "user/valid.html")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError) as e:
        return render(request, "user/invalid.html")


from django.contrib.auth.decorators import login_required

def resend_verification(request):
    user = request.user

    if user.is_authenticated:
        if not user.email_verified:
            # Generate verification token
            token = default_token_generator.make_token(user)

            # Generate verification link
            current_site = get_current_site(request)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = reverse('verify_email', kwargs={'uidb64': uidb64, 'token': token})
            verification_link = f'{current_site.domain}{verification_link}'

            # Send verification email asynchronously
            send_verification_email.delay(user.email, verification_link)

            # Return success response or redirect to a success page
            return HttpResponse("Verification email has been resent.")
        else:
            return HttpResponse("Your email is already verified.")
    else:
        # Handle the case when the user is not authenticated
        return HttpResponse("Please log in to resend the verification email.")



def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('home')
    else:
        form = ProfileUpdateForm()
    return render(request, 'user/profile.html', {'pform': form})

def logout_view(request):

    logout(request)
    return redirect('login')

@api_view(['POST'])
def obtain_auth_token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid username or password'})
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class FollowCreateAPIView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(Q(follower=user) | Q(following=user))
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     followers = queryset.filter(following=self.request.user).values('follower', 'follower__username')
    #     following = queryset.filter(follower=self.request.user).values('following', 'following__username')
    #
    #     follower_count = followers.count()
    #     following_count = following.count()
    #
    #     response_data = {
    #         'followers_count': follower_count,
    #         'following_count': following_count,
    #         'followers': list(followers),
    #         'following': list(following),
    #     }
    #
    #     return Response(response_data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        followers = queryset.filter(following=self.request.user).values('follower', 'follower__username')
        following = queryset.filter(follower=self.request.user).values('following', 'following__username')

        follower_count = followers.count()
        following_count = following.count()

        response_data = {
            'followers_count': follower_count,
            'following_count': following_count,
            'followers': [{'id': follower['follower'], 'username': follower['follower__username']} for follower in
                          followers],
            'following': [{'id': follow['following'], 'username': follow['following__username']} for follow in
                          following],
        }

        return Response(response_data)


    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    def destroy(self, request, *args, **kwargs):
        unfollow_id = kwargs.get("id")
        if unfollow_id:
            user = request.user
            try:
                follow = Follow.objects.get(follower=user, following_id=unfollow_id)
                follow.delete()
                return Response({'message': 'User unfollowed successfully.'}, status=status.HTTP_200_OK)
            except Follow.DoesNotExist:
                return Response({'error': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No user ID provided to unfollow.'}, status=status.HTTP_400_BAD_REQUEST)

# def resend_verification_email(request):
#     if request.method == 'GET':
#         email = request.GET.get('email')
#
#         # Check if email is provided
#         if email:
#             # Generate verification token
#             user = User.objects.get(email=email)
#             token = default_token_generator.make_token(user)
#
#             # Generate verification link
#             current_site = get_current_site(request)
#             uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#             verification_link = reverse('verify_email', kwargs={'uidb64': uidb64, 'token': token})
#             verification_link = f'{current_site.domain}{verification_link}'
#
#             # Send verification email asynchronously
#             send_verification_email.delay(user.email, verification_link)
#
#             # Redirect to success page or display a success message
#             return render(request, 'user/success.html')
#
#     # Handle invalid or missing email
#     return render(request, 'user/verification_email_invalid.html')

