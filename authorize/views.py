from datetime import timedelta, datetime

import pytz
from django.contrib.auth import authenticate

# Create your views here.
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from authorize.authentication import VALIDATE_DAYS
from authorize.serializers import UserSerializer

class Account(APIView):

    def post(self, request, format=None):
        id = request.data.get('id', None)
        password = request.data.get('password', None)
        user = authenticate(username=id, password=password)
        if user == None:
            return Response({'message': '로그인에 실패하였습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)

        d = timedelta(days=VALIDATE_DAYS)

        end = (token.created + d).replace(tzinfo=pytz.UTC)
        start = (token.created).replace(tzinfo=pytz.UTC)
        dest = (datetime.now()).replace(tzinfo=pytz.UTC)

        if start > dest or dest > end:
            token.delete()
            return Response({"message": "토큰이 만료 되었습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        token.created = timezone.now()
        token.save()
        response = {}

        response["token"] = token.key
        response["created"] = token.created
        return Response(response, status=status.HTTP_200_OK)

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self, request, format=None):
        token = request.META.get('HTTP_AUTHORIZATION')

        if token == None:
            return Response({'message': '토큰 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = token.split(' ')[1]
            token = Token.objects.get(key=token)

            d = timedelta(days=VALIDATE_DAYS)

            end = (token.created + d).replace(tzinfo=pytz.UTC)
            start = (token.created).replace(tzinfo=pytz.UTC)
            dest = (datetime.now()).replace(tzinfo=pytz.UTC)

            if start > dest or dest > end:
                token.delete()
                return Response({"message": "토큰이 만료 되었습니다."}, status=status.HTTP_401_UNAUTHORIZED)

            token.created = timezone.now()
            token.save()
        except:
            return Response({'message': '사용자가 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'user':UserSerializer(token.user).data}, status.HTTP_200_OK)

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def patch(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if token == None:
            return Response({'message': '토큰 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = token.split(' ')[1]
            token = Token.objects.get(key=token)
            token.delete()

        except:
            return Response({'message': '로그아웃 실패'}, status=status.HTTP_401_UNAUTHORIZED)


        return Response({'message': '성공적으로 로그아웃 하였습니다.'}, status.HTTP_200_OK)


