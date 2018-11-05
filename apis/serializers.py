from django.contrib.auth.models import User
from authentication.models import UserProfile 
from rest_framework import serializers
from django.conf import settings 
import jwt

class RegisterSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')
        extra_kwargs = {'password': {'write_only': True}}


    def get_token(self, obj):
        return obj.userprofile.token 

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        encoded_token = jwt.encode({'user_id': user.id}, 'SECRET', algorithm='HS256')
        user.userprofile.token = encoded_token
        user.save()
        return user
