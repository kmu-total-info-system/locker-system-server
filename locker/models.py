from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Block(models.Model):
    class Meta:
        verbose_name_plural = "타일 하나"

    BLOCK_TYPES = (
        (1, 'hallway'),
        (2, 'area'),
        (3, 'room'),
        (4, 'locker'),
        (5, 'stairs'),
    )
    LOCKER_STATES = (
        (1, '신청가능'),
        (2, '고장'),
        (3, '주인 있음'),
    )
    DIRECTIONS = (
        (1, '왼쪽'),
        (2, '위쪽'),
        (3, '오른쪽'),
        (4, '아랫쪽'),
    )
    type = models.SmallIntegerField(verbose_name="타입", choices=BLOCK_TYPES)
    width = models.IntegerField(verbose_name="너비")
    height = models.IntegerField(verbose_name="높이")

    value = models.CharField(verbose_name="내용(stairs제외)", blank=True, null=True, max_length=32)

    color = models.CharField(verbose_name="색깔(locker,area)", blank=True, null=True, max_length=16)
    link = models.ForeignKey('Sheet', verbose_name="연결(area)", blank=True, null=True, on_delete=models.CASCADE)

    state = models.SmallIntegerField(verbose_name="사물함 상태(locker)", null=True, blank=True, choices=LOCKER_STATES)

    direction = models.SmallIntegerField(verbose_name="계단 방향(stairs)", null=True, blank=True, choices=DIRECTIONS)

    def __str__(self):
        return self.value


class Sheet(models.Model):
    class Meta:
        verbose_name_plural = "시트"

    blocks = models.ManyToManyField('Block', related_name="block_sheet", null=True, blank=True)

    def __str__(self):
        return ", ".join([str(block) for block in self.blocks.all()])

class Transaction(TimeStampedModel):
    class Meta:
        verbose_name_plural="신청"
        ordering = ('-created',)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=('사용자'),
        on_delete=models.CASCADE,
        related_name='transaction_user'
    )

    block = models.ForeignKey(
        'Block', related_name="transaction_block", on_delete=models.CASCADE,verbose_name="타일 하나"
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=('IP Address'),
        null=True,
        blank=True
    )

    user_agent = models.CharField(
        verbose_name=('HTTP User Agent'),
        max_length=300,
        null=True,
        blank=True
    )

    def __str__(self):
        return '%s %s' % (self.user, self.ip_address)

    pass