from django.contrib.auth.models import User
from authentication.models import UserProfile 
from rest_framework import serializers
from django.conf import settings 
import jwt
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    # token = serializers.CharField(source='get_token', read_only=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    
    def get_token(self):
        return 'fsdfsd'

    # def get_cleaned_data(self):
    #     return {
    #         'username': self.validated_data.get('username', ''),
    #         'password': self.validated_data.get('password', ''),
    #         'email': self.validated_data.get('email', ''),
    #         'token': '656565',
    #     }

    def create(self, request):
        username = self.validated_data.get('username') 
        email = self.validated_data.get('email') 
        password = self.validated_data.get('password') 

        user = User.objects.create_user(username = username, password=password,email=email)
        encoded_token = jwt.encode({'user_id': user.id}, 'SECRET', algorithm='HS256')

        user.userprofile.token = encoded_token
        user.save()
        return user

