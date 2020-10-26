from django.db import models
from django.urls import reverse

from datetime import date


# Create your models here.
class Photo(models.Model):
    """猫猫相片的数据库模型"""
    image = models.ImageField(
        '图像',
        upload_to='image/'
        )
    title = models.CharField('标题', blank=True, max_length=8)
    description = models.TextField('图片描述', blank=True)
    author = models.ForeignKey(
        'campus.User', 
        verbose_name='拍摄者', 
        on_delete=models.SET_NULL,
        null = True,
        blank = True,
        related_name = 'photos',
        related_query_name = 'photo'
        )
    author_name = models.CharField('拍摄者名称', max_length=16, blank=True)
    date = models.DateField('拍摄日期', default=date.today, null=True, blank=True)
    
    cats = models.ManyToManyField(
        'cat.Cat',
        verbose_name='出镜猫猫们',
        related_name='photos',
        related_query_name='photo'
    )

    class Meta:
        verbose_name = '相片'
        verbose_name_plural = '相片'

    def __str__(self):
        name = ''
        if self.cats.count() < 3:
            for cat in self.cats.all():
                name = name + str(cat) + '-'
        else:
            cats = self.cats.all()
            name = str(cats[0]) + '-...-' + str(cats[1]) + '-'

        if self.title:
            name = name + self.title + '-'
        if self.date:
            name = name + str(self.date.year) + '-'
        
        return name[:-1]

    def get_absolute_url(self):
        return reverse('file:photo', {'pk': self.pk})

    def get_author(self):
        """拍摄者名称"""
        if self.author:
            return self.author.username
        elif self.author_name:
            return self.author_name
        else:
            return '佚名'

