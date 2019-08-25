from datetime import timedelta, datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from locker.models import Sheet
from locker.serializers import SheetSerializer


class Locker(APIView):
    def get(self, request, id=None, format=None):
        try:
            sheets = Sheet.objects.get(id=id)
            return Response(SheetSerializer(sheets).data, status.HTTP_200_OK)
        except:
            return Response({}, status.HTTP_404_NOT_FOUND)


    # @authentication_classes((TokenAuthentication,))
    # @permission_classes((IsAuthenticated,))
    # def patch(self, request):
    #     token = request.META.get('HTTP_AUTHORIZATION')
    #
    #     if token == None:
    #         return Response({'message': '사용자가 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    #
    #     try:
    #         token = token.split(' ')[1]
    #         token = Token.objects.get(key=token)
    #         token.delete()
    #
    #     except:
    #         return Response({'message': '로그아웃 실패'}, status=status.HTTP_401_UNAUTHORIZED)
    #
    #
    #     return Response({'message': '성공적으로 로그아웃 하였습니다.'}, status.HTTP_200_OK)
    #
    #
