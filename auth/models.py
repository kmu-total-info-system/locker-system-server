from django.db import models


# Create your models here.
class Account(models.Model):
    user_id = models.CharField(max_length=9, verbose_name="학번")
    name = models.CharField(max_length=7, verbose_name="이름")
    ssn = models.CharField(max_length=40, verbose_name="주민등록번호")
    college = models.CharField(max_length=40, verbose_name="대학명")
    school = models.CharField(max_length=40, verbose_name="스쿨이름")
    time = models.CharField(max_length=10, verbose_name="주/야")
    major = models.CharField(max_length=10, verbose_name="전공")
    date = models.CharField(max_length=40, verbose_name="입학일자")
    state = models.CharField(max_length=10, verbose_name="재적상태")
    grade = models.IntegerField(verbose_name="학년")
    passwd = models.CharField(max_length=50, verbose_name="비번")
