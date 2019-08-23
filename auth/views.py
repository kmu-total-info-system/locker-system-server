from django.shortcuts import render

# Create your views here.
from ktis_parser import ktis_parser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models


class Account(APIView):

    def post(self, request, format=None):
        id = request.data.get('id',None)
        passwd = request.data.get('passwd',None)
        print(id,passwd)
        res = ktis_parser.parseInfo(id,passwd)
        res['content']['grade'] = int(res['content']['grade'][0])
        print(res)
        account = models.Account()

        res = ktis_parser.parseSimpleGrade(id,passwd)
        print(res)
        # mac_adderss = request.data.get('mac_address',None)
        # if code != None:
        #     accounts = Account.objects.filter(code=code)
        #     if len(accounts) == 1:
        #         if accounts[0].mac_address == None:
        #             accounts[0].mac_address = mac_adderss
        #             accounts[0].save()
        #             return Response({'code':code,'mac_address':mac_adderss}, status=status.HTTP_201_CREATED)
        #         elif accounts[0].mac_address == mac_adderss:
        #             return Response({'code':code,'mac_address':mac_adderss}, status=status.HTTP_202_ACCEPTED)
        #         else:
        #             return Response({'message': 'mac 주소 정보가 일치하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        #
        #     elif len(accounts) > 1:
        #         return Response({'message': '중복정보 입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        #     else:
        #         return Response({'message': '존재하지 않는 정보 입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        #
        # else:
        #     return Response({'message':'코드가 입력 되지 않았습니다.'},status=status.HTTP_400_BAD_REQUEST)
        return Response({},status=status.HTTP_200_OK)

