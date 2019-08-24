from django.contrib.auth import authenticate
from django.shortcuts import render

# Create your views here.
from ktis_parser import ktis_parser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authorize.serializers import UserSerializer
from . import models


class Account(APIView):

    def post(self, request, format=None):
        id = request.data.get('id',None)
        password = request.data.get('password',None)
        user = authenticate(username=id,password=password)

        if user == None:
            return Response({'message':'로그인에 실패하였습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(UserSerializer(user).data,status=status.HTTP_200_OK)

