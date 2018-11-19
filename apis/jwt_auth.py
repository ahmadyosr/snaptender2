from rest_framework import status, exceptions
from django.http import HttpResponse
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.contrib.auth.models import User
import jwt
import json


class TokenAuthentication(BaseAuthentication):

    model = None

    def get_model(self):
        return User

    def authenticate(self, request):
        token = request.data.get('token')

        if token : 
            return self.authenticate_credentials(token)

        msg = 'Invalid token header'
        raise exceptions.AuthenticationFailed(msg)




    def authenticate_credentials(self, token):
        model = self.get_model()
        payload = jwt.decode(token, "SECRET", algorithm='HS256')
        user_id = payload['user_id']
        msg = {'Error': "Token mismatch",'status' :"401"}
        user = User.objects.get(
            id=user_id
        )

        try:
            
            user = User.objects.get(
                id=user_id
            )

            if str(user.userprofile.token) != str(token.encode()):
                raise exceptions.AuthenticationFailed(msg)
               
        except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:
            return HttpResponse({'Error': "Token is invalid"}, status="403")

        except User.DoesNotExist:
            return HttpResponse({'Error': "Internal server error"}, status="500")


        return (user, token)

    def authenticate_header(self, request):
        return 'Token'