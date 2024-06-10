from rest_framework import serializers
from authentication.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from account.utils import Util
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.response import Response



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['email', 'name', 'first_name', 'last_name', 'password', 'password2', 'tc', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role', 'user')
        user = User.objects.create_user(**validated_data, role=role)
        return user



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name','first_name','last_name', 'role']



class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    new_password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    
    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password2 = attrs.get('new_password2')
        user = self.context.get('user')
        
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect.")
        
        if new_password != new_password2:
            raise serializers.ValidationError("New password and confirm password do not match.")
        
        return attrs
    
    def save(self, **kwargs):
        user = self.context.get('user')
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()

# from django.contrib.auth.password_validation import validate_passwor 
# class UserChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)
#     new_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True, validators=[validate_password])
#     confirm_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)

#     class Meta:
#         fields = ['old_password', 'new_password', 'confirm_password']

#     def validate(self, attrs):
#         old_password = attrs.get('old_password')
#         new_password = attrs.get('new_password')
#         confirm_password = attrs.get('confirm_password')
#         user = self.context.get('user')

#         if not user.check_password(old_password):
#             raise serializers.ValidationError({"old_password": "Old password is not correct"})

#         if new_password != confirm_password:
#             raise serializers.ValidationError({"confirm_password": "New passwords do not match"})

#         return attrs

#     def save(self, **kwargs):
#         user = self.context.get('user')
#         user.set_password(self.validated_data['new_password'])
#         user.save()
#         return user



class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f'http://127.0.0.1:5501/reset-password.html?uid={uid}&token={token}'
            email_subject = "Reset Your Password"
            email_body = render_to_string('confirm_email.html', {'confirm_link': link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            try:
                email.send()
            except Exception as e:
                print(f"Error sending email: {e}")
            return Response("Check your mail for confirmation")
        else:
            raise serializers.ValidationError('You are not a Registered User')



class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        print(uid)
        token = self.context.get('token')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError('Token is not Valid or Expired')
