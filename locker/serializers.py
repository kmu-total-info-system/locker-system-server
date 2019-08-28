from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from locker.models import Sheet, Block, Transaction

UserModel = get_user_model()


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'


class SheetSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True)

    class Meta:
        model = Sheet
        fields = '__all__'


class SheetSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        exclude = ('blocks',)


class TransactionSerializer(serializers.ModelSerializer):
    block = BlockSerializer()
    class Meta:
        model = Transaction
        fields = '__all__'
