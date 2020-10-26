from django.db import models
from django.urls import reverse
from django.conf import settings

from utilties import ChoiceList
from datetime import date

#from . import

# Create your models here.
class Cat(models.Model):
    """猫猫的数据库模型"""

    BIRTH_MONTH_CHOICES = ChoiceList([f'{i+1}' for i in range(12)], '春天', '夏天', '秋天', '冬天', null=True)
    BIRTH_DAY_CHOICES = ChoiceList([f'{i+1}' for i in range(31)], '上旬', '中旬', '下旬', null=True)
    CAT_TYPE_CHOICES = ChoiceList('纯白', '纯黑', '奶牛', '狸花', '狸白', '纯橘', '橘白', '三花', '玳瑁', '其他')
    STATUS_CHOICES = ChoiceList('在校流浪', '失踪', '离世', '已领养', '住院', null='状态未知')
    SOURCE_CHOICES = ChoiceList('流浪后代', '弃养', '校外流浪猫', null=True)

    name = models.CharField('名字', max_length=16, blank=True)
    gender = models.BooleanField('性别', null=True, blank=True, choices=[(False, '女'), (True, '男'), (None, '未知')])
    status = models.PositiveSmallIntegerField(
        '状态', null=True, blank=True, 
        choices=STATUS_CHOICES.to_turples(),
        default=STATUS_CHOICES.get_val('在校流浪')
        )
    campus = models.ForeignKey(
        'campus.Campus', 
        verbose_name='校区', 
        related_name='cats',
        related_query_name='cat',
        on_delete=models.CASCADE
        )
    description = models.TextField('描述', blank=True, max_length=512)
    source = models.PositiveSmallIntegerField('来源', null=True, blank=True, choices=SOURCE_CHOICES.to_turples())
    birth_year = models.PositiveSmallIntegerField('出生年', null=True, blank=True)
    birth_month = models.PositiveSmallIntegerField('出生月', null=True, blank=True, choices=BIRTH_MONTH_CHOICES.to_turples())
    birth_day = models.PositiveSmallIntegerField('出生日', null=True, blank=True, choices=BIRTH_DAY_CHOICES.to_turples())
    long_hair = models.BooleanField('长毛', null=True, blank=True, choices=[(True, '长毛'), (False, '短毛'), (None, '未知')])
    cat_type = models.PositiveSmallIntegerField('毛色', choices=CAT_TYPE_CHOICES.to_turples())
    neutered = models.BooleanField('绝育', null=True, blank=True, choices=[(True, '已绝育'), (False, '未绝育'), (None, '未知')])
    last_update = models.DateField('最近更新', null=True)
    documented_date = models.DateField('档案创建', null=True)
    parent = models.ForeignKey(
        "campus.User", 
        verbose_name='紧急联系人',
        on_delete=models.SET_NULL,
        related_name='kids',
        related_query_name='kid',
        null=True,
        blank=True
        )
    mom = models.ForeignKey(
        'cat.Cat',
        verbose_name='猫妈',
        limit_choices_to={'gender': 0},    # 只能选择母猫！
        related_name='kids',
        related_query_name='kid',
        null=True,
        blank=True,
        on_delete =models.SET_NULL
    )
    avatar = models.ForeignKey(
        'file.Photo',
        verbose_name='证件照',
        related_name='avatar_cat',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    cover_photo = models.ForeignKey(
        'file.Photo',
        verbose_name='封面照',
        related_name='cover_photo_cat',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    locations = models.ManyToManyField(
        "campus.Location", 
        verbose_name='活动位置',
        related_name='cats',
        related_query_name='cat',
        blank=True
        )


    class Meta:
        verbose_name = "猫猫"
        verbose_name_plural = "猫猫"
        constraints = [
            models.UniqueConstraint(fields=['name', 'campus'], name='unique_name')    # 同校区不可同名
        ]
        ordering = ['pk']

    def __str__(self):
        name = f'{str(self.campus)}-{self.name if self.name else ("未命名"+str(self.pk))}'
        if self.status != self.STATUS_CHOICES.get_val('在校流浪'):
            return f'{name}({self.get_status_display()})'
        else:
            return name

    def get_absolute_url(self):
        return reverse("cat:detail", kwargs={"pk": self.pk})

    @property
    def default_avatar(self):
        """返回默认头像"""
        return settings.DEFAULT_CAT_AVATAR

    @property
    def age(self):
        """估计猫猫的年龄"""
        if not self.birth_year:
            return '未知'
        elif self.get_status_display() == '离世':
            return '已离世'
        else:
            today = date.today()
            birthday = date(self.birth_year, 6, 30)

            # 获得大致年龄（天）
            if self.birth_month:
                month = self.get_birth_month_display()
                real_month = 0
                if not month.isdecimal():
                    # 估计月份
                    real_month = {'春天': 3, '夏天': 6, '秋天': 9, '冬天': 12}.get(month)
                    birthday = birthday.replace(month=real_month, day=15)
                else:
                    birthday = birthday.replace(month=int(month))
                    
                    day = self.get_birth_day_display()
                    real_day = 0
                    if not day.isdecimal():
                        # 估计日期
                        real_day = {'上旬': 5, '中旬': 15, '下旬': 25}.get(day)
                        birthday = birthday.replace(day=real_day)
                    else:
                        birthday = birthday.replace(month=int(day))

        days = (today - birthday).days

        # 将天数转换为人性化单位表示
        if days < 2*30:
            age = str(round(days / 7)) + '周'
        else:
            months = round(days / 30)
            
            if months < 10:
                age = str(months) + '个月'
            elif months > 12*5:
                age = str(round(months / 12)) + '岁'
            else:
                years, half = divmod(round(months/6), 2)
                age = str(years) + '岁' + ('半' if half else '')

        # # 若有估计则加上约
        # if real_month or real_day:
        #     age  = '约' + age

        return age



class Entry(models.Model):
    """记录猫咪状态的条目"""
    key = models.CharField('键', max_length=16)
    description = models.TextField('描述', blank=True)
    date = models.DateField('日期')
    cat = models.ForeignKey(
        Cat,
        verbose_name='猫猫',
        on_delete=models.CASCADE,
        related_name='entries',
        related_query_name='entry'
        )
    user = models.ForeignKey(
        'campus.User', 
        verbose_name='操作者', 
        on_delete=models.SET_NULL,
        null=True
        )

    class Meta:
        verbose_name = '记录'
        verbose_name_plural = '记录'
        indexes = [
            models.Index(fields=['cat', 'date']),
        ]
        ordering = ['date']

    def __str__(self):
        return f'{self.cat!s}-{self.key}-{self.date}'