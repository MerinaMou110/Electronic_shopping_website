from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from authentication.serializers import (
    SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, 
    UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
)
from django.contrib.auth import authenticate
from authentication.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str
from django.contrib.auth.tokens import default_token_generator
from authentication.models import User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = f'https://electronic-shopping-website-as07.onrender.com/api/user/activate/{uid}/{token}/'
        email_subject = 'Activate your account'
        email_body = render_to_string('activation_email.html', {'activation_link': link})
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        try:
            email.send()
        except Exception as e:
            print(f"Error sending email: {e}")
        return Response({'msg': 'Registration successful. Please check your email to activate your account.'}, status=status.HTTP_201_CREATED)

class ActivateAccountView(APIView):
    def get(self, request, uidb64, token, format=None):
        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'msg': 'Account activated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Activation link is invalid'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'role': user.role, 'user_id': user.id}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)




from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializers import UserProfileSerializer

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
    


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link sent. Please check your email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        # uid = request.data.get('uid')
        # token = request.data.get('token')
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            # Manually blacklist the token
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError:
            # Fallback for manually blacklisting the token
            try:
                BlacklistedToken.objects.create(token=token)
                return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)