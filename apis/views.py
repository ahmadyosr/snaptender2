from django.shortcuts import render
from catalogue.models import Snippet, Category
from django.contrib.auth.models import User 
from catalogue.serializers import TenderSnippetSerializer, CategorySerializer
from apis.serializers import RegisterSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Q
import jwt
# Create your views here.

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.filter(Q(is_tender=True) | Q(is_auction=True))[:100]
    serializer_class = TenderSnippetSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class Register(APIView):
    """
    Login .
    """
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide username/password/"}, status="400")

        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username, password=password)

        except User.DoesNotExist:

            serializer = RegisterSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.save()
                print('USER ---------' , user)

                if user:
                    return Response(serializer.data, status=200)
            else : 
                return Response(serializer.errors, status=200)

class Login(APIView):
    # refresh token/ assign new token

    def post(self, request, *args, **kwargs):
        # if not request.data:
        #     return Response({'Error': "Please provide username/password"}, status="400")
        
        # username = request.data['username']
        # password = request.data['password']
        # try:
        #     user = User.objects.get(username=username, password=password)
        # except User.DoesNotExist:
        #     return Response({'Error': "Invalid username/password"}, status="400")
        # if user:
            
        #     payload = {
        #         'id': user.id,
        #         'email': user.email,
        #     }
        #     jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}

        #    return HttpResponse(
        #       json.dumps(jwt_token),
        #       status=200,
        #       content_type="application/json"
        #     )
        # else:
        #     return Response(
        #       json.dumps({'Error': "Invalid credentials"}),
        #       status=400,
        #       content_type="application/json"
        #     )
        pass


class Logout(APIView):
    """
    Logout .
    # simply delete the token to force a login

    """
    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
