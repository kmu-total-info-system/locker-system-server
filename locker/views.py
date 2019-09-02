from datetime import timedelta, datetime

from django.db.models import Q
from django.forms import model_to_dict
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from locker import models
from locker.models import Sheet, Block, Time, Permission
from locker.serializers import SheetSerializer, SheetSimpleSerializer, TransactionSerializer

from ipware.ip import get_ip


class Locker(APIView):
    def get(self, request, id=None, format=None):
        try:
            sheet = Sheet.objects.get(id=id)
            return Response(SheetSerializer(sheet).data, status.HTTP_200_OK)
        except:
            sheets = Sheet.objects.all()
            return Response(SheetSimpleSerializer(sheets, many=True).data, status.HTTP_200_OK)


class Transaction(APIView):
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self, request):

        token = request.META.get('HTTP_AUTHORIZATION')
        if token == None:
            return Response({'message': '토큰 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = token.split(' ')[1]
            token = Token.objects.get(key=token)
        except:
            return Response({'message': '사용자가 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        user = token.user
        try:
            transaction = models.Transaction.objects.get(user=user)
            other = models.Transaction.objects.filter(block_id=transaction.block_id)
            if len(other) > 1 and other[0] != transaction:
                transaction.delete()
                return Response({'message': '신청한 사물함이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)

        except:
            return Response({'message': '신청한 사물함이 없습니다.'}, status=status.HTTP_204_NO_CONTENT)

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)

    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def post(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == None:
            return Response({'message': '토큰 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            token = token.split(' ')[1]
            token = Token.objects.get(key=token)
        except:
            return Response({'message': '사용자가 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        user = token.user
        block_id = request.data.get('block', None)
        transaction = models.Transaction.objects.filter(user=user)
        if len(transaction) != 0:
            return Response({'message': '이미 신청한 사용자 입니다.'}, status=status.HTTP_400_BAD_REQUEST)


        time = models.Time.objects.first()
        if time.end < timezone.localtime() or time.start > timezone.localtime():
            return Response({'message': '신청기간이 아닙니다.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        block = Block.objects.get(id=block_id)
        if block.state != 1:
            return Response({'message': '신청 불가능한 사물함입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if block.parent != None:
            permission_ids = []
            permissions = list(time.permission.all().values())
            for p in permissions:
                if p["block_id"] == block.parent_id:
                    permission_ids.append(p["id"])
            dict_user = model_to_dict(user)
            permission_status = False
            for permission_id in permission_ids:
                check = True
                for key, value in model_to_dict(Permission.objects.get(id=permission_id).pivot).items():
                    if value != None and key != 'user_id' and key != 'name' and key != 'password' and key != 'id' and key != 'is_admin':
                        if dict_user[key] != value:
                            check=False
                if check:
                    permission_status = True
                    break
            if permission_status != True:
                return Response({'message': '해당 사용자는 권한이 없습니다. '},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': '사물함 정보가 올바르지 않습니다.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        block.state = 3
        block.save()

        ip_address = get_ip(request)
        user_agent = request.META['HTTP_USER_AGENT']
        check = models.Transaction.objects.filter(block_id=block_id)
        if len(check) > 0:
            return Response({'message': '신청 불가능한 사물함입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            transaction = models.Transaction(user=user, block_id=block_id, ip_address=ip_address, user_agent=user_agent)
            transaction.save()
        except:
            return Response({'message': '신청 불가능한 사물함입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

class Time(APIView):
    def get(self,request):
        return Response({'time':timezone.localtime()}, status=status.HTTP_200_OK)