from ktis_parser import ktis_parser

from django.contrib.auth import get_user_model, user_logged_in
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()
VALIDATE_DAYS = 30

class KtisBackend(ModelBackend):
    def authenticate(self, request,username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        res = ktis_parser.parseInfo(username, password)
        if not bool(res['status']):
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
            else:
                if user.check_password(password):
                    return user
                else:
                    return res['content']
        else:
            try:
                user = UserModel._default_manager.get_by_natural_key(username)
            except:
                user = UserModel.objects.create_user(user_id=username,
                                                     password=password,
                                                     extra_fields=res['content'])
            return user

