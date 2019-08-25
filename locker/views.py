from datetime import timedelta, datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from locker.models import Sheet
from locker.serializers import SheetSerializer, SheetSimpleSerializer


class Locker(APIView):
    def get(self, request, id=None, format=None):
        try:
            sheet = Sheet.objects.get(id=id)
            return Response(SheetSerializer(sheet).data, status.HTTP_200_OK)
        except:
            sheets = Sheet.objects.all()
            return Response(SheetSimpleSerializer(sheets,many=True).data, status.HTTP_404_NOT_FOUND)


