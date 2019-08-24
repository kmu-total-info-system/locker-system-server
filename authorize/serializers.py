from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        exclude = ('is_admin','password','groups','user_permissions','is_superuser')

    # def create(self, validated_data):
    #     validated_data['is_superuser']=False
    #
    #     if validated_data.get('password'):
    #         validated_data['password'] = make_password(
    #             validated_data['password']
    #         )
    #     if validated_data.get('groups') != None:
    #         validated_data.pop("groups")
    #     if validated_data.get('user_permissions') != None:
    #         validated_data.pop("user_permissions")
    #
    #     user = UserModel.objects.create_user(**validated_data)
    #     return user
