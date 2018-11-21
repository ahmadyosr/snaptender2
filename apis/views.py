from django.shortcuts import render
from catalogue.models import Snippet, Category
from django.contrib.auth.models import User 
from catalogue.serializers import TenderSnippetSerializer, CategorySerializer, SnippetSerializer
from apis.serializers import RegisterSerializer, PreferencesSerializer, LoginSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from django.db.models import Q
import jwt
from django.contrib.auth import authenticate


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.filter(Q(is_tender=True) | Q(is_auction=True))[:100]
    serializer_class = TenderSnippetSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []


class SnippetDetail(APIView):
    queryset = Snippet.objects.filter(Q(is_tender=True) | Q(is_auction=True))[:100]
    serializer_class = TenderSnippetSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        instance = Snippet.objects.get(id=kwargs.get('pk'))

        
        serializer = self.serializer_class(instance=instance, data={})

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else : 
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)



class LoginApi(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [] 
    

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')


        if not email or not password:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email, password= password)


        if not user : 
            return Response({'error': 'User Does Not Exist'},
                            status=status.HTTP_400_BAD_REQUEST)
        else : 
            serializer = LoginSerializer(user, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else : 
                return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class RegisterApi(APIView):
    """
    Login .
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [] 
    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide email/password/"}, status="400")


        serializer = RegisterSerializer(data=request.data)

        email = request.data.get('email')
        password = request.data.get('password')

        if (not email) or (not password):
            return Response(status=400)

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:

            if serializer.is_valid():
                user = serializer.save()

                if user:
                    return Response(serializer.data, status=201)
            else : 
                return Response(serializer.errors, status=400)
        
# class FavoriteList(APIView):
#     def post(self, request, *args, **kwargs):

class FavoriteApi(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        token = request.data.get('token')
        payload = jwt.decode(token, "SECRET", algorithm='HS256')
        user_id = payload['user_id']
        user = User.objects.get(id=user_id)


        snippet_id = kwargs.get('pk')
        snippet = Snippet.objects.filter(is_tender=True).get(id = snippet_id)

        snippets = user.userprofile.snippets.all()

        # user.snippets.remove(id=1)
        if snippet in snippets:
            user.userprofile.snippets.remove(snippet)
            return Response(status = 200)
        else :
            user.userprofile.snippets.add(snippet)
            return Response(status = 200)


class FavoriteList(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        token = self.request.data.get('token')
        payload = jwt.decode(token, "SECRET", algorithm='HS256')
        user_id = payload['user_id']
        user = User.objects.get(id=user_id)

        snippets = user.userprofile.snippets.all()

        serializer = SnippetSerializer(snippets, many=True,)
        return Response(serializer.data, status=200)




class AddPreferencesList(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = PreferencesSerializer(data=request.data)

        if serializer.is_valid():
            # serializer.save()
            # print(serializer.data)
            serializer.save()
            
        return Response(serializer.data, status=200)


class PreferencesList(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        token = request.data['token']
        payload = jwt.decode(token, "SECRET", algorithm='HS256')
        user_id = payload['user_id']
        user = User.objects.get(id=user_id)
        
        serializer = PreferencesSerializer(instance=user.userprofile)

        return Response(serializer.data, status=200)
