from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, user_id, password, extra_fields):
        kwargs = extra_fields.copy()
        kwargs['grade'] = int(kwargs['grade'][0])
        user = self.model(
            **kwargs
        )
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, user_id, password,name):
        user = self.model(
            user_id=user_id, password=password,name = name
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser=True
        user.set_password(password)
        user.save(using=self._db)
        return user


class AuthUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = "유저정보"

    user_id = models.CharField(max_length=9, verbose_name="학번")
    name = models.CharField(max_length=7, verbose_name="이름")
    ssn = models.CharField(max_length=40, verbose_name="주민등록번호",blank=True,null=True)
    college = models.CharField(max_length=40, verbose_name="대학명",blank=True,null=True)
    school = models.CharField(max_length=40, verbose_name="스쿨이름",blank=True,null=True)
    time = models.CharField(max_length=10, verbose_name="주/야",blank=True,null=True,choices=(('주간','주간'),('야간','야간')))
    major = models.CharField(max_length=10, verbose_name="전공",blank=True,null=True)
    date = models.CharField(max_length=40, verbose_name="입학일자",blank=True,null=True)
    status = models.CharField(max_length=10, verbose_name="재적상태",blank=True,null=True)
    grade = models.IntegerField(verbose_name="학년",blank=True,null=True)
    password = models.CharField(max_length=256, verbose_name="비번")

    is_active = models.BooleanField(verbose_name="활성화", default=False)
    is_admin = models.BooleanField(verbose_name="어드민 계정 여부", default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'user_id'
    PASSWORD_FIELD = 'password'
    REQUIRED_FIELDS = ['name',]

    def __str__(self):
        ret = self.user_id
        if self.name != None:
            ret+=" "+self.name
        return ret

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
