
from django.urls import path,include
from authentication.views import  SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView,ActivateAccountView,LogoutView

urlpatterns = [
     path('register/', UserRegistrationView.as_view(), name='register'),
     path('login/', UserLoginView.as_view(), name='login'),
     path('logout/', LogoutView.as_view(), name='logout'),
     path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
]