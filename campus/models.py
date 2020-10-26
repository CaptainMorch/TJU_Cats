from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass


class Campus(models.Model):
    '''校区的数据库模型'''
    name = models.CharField('简称', max_length=4)
    full_name = models.CharField('全名', max_length=16)
    longitude = models.FloatField('经度')
    latitude = models.FloatField('纬度')
    # Do not use DecimalField herebecause it's not json serializable
    zoom_level = models.PositiveSmallIntegerField('地图缩放级别')
    
    class Meta:
        verbose_name = '校区'
        verbose_name_plural = '校区'

    def __str__(self):
        return self.name


class Location(models.Model):
    """校内猫猫活动的位置"""
    name = models.CharField('名称', max_length=32)
    campus = models.ForeignKey(
        Campus,
        verbose_name='校区',
        related_name='locations',
        related_query_name='location',
        on_delete=models.CASCADE
        )
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7)

    class Meta:
        verbose_name = '位置'
        verbose_name_plural = '位置'

    def __str__(self):
        return str(self.campus) + self.name
