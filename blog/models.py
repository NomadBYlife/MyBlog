from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.urls import reverse
from django.contrib.auth.models import User, AbstractUser
from slugify import slugify


class Bloger(models.Model):
    pseudonym = models.OneToOneField(User,on_delete=models.CASCADE, unique=True, verbose_name='псевдоним')
    slug = models.SlugField(max_length=50, db_index=True, verbose_name='слаг')
    first_name = models.CharField(max_length=50, verbose_name='имя блогера')
    last_name = models.CharField(max_length=50, verbose_name='фамилия блогера')
    bio = models.TextField(max_length=200,verbose_name='инфо о блогере',null=True)
    age = models.IntegerField(verbose_name='Возраст',null=True)
    is_published = models.BooleanField(default=True, verbose_name='статус блогера')

    def __str__(self):
        return self.pseudonym.username

    class Meta():
        ordering = ('id',)
        verbose_name = 'блогер'
        verbose_name_plural = 'блогеры'

    def save(self, *args, **kwargs):
        if not self.slug:
            pseudonim = str(self.pseudonym)
            self.slug = slugify(pseudonim)
        return super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Bloger.objects.create(pseudonym=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.bloger.save()


class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='название блога')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='слаг')
    discription = models.TextField(blank=True, verbose_name='описание блога')
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True, verbose_name='картинка')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=False, verbose_name='статус публикации')
    author = models.ForeignKey(Bloger, on_delete=models.CASCADE, verbose_name='автор блога')

    def __str__(self):
        return self.title

    class Meta():
        ordering = ('-date_created', 'title')
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('show_blog', kwargs={'slug':self.slug})



class Comment(models.Model):
    discription = models.TextField(verbose_name='коментарий')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(verbose_name='статус публикации',default=True)
    author = models.CharField(max_length=300, verbose_name='автор',null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,verbose_name='блог')

    def __str__(self):
        return self.discription[0:50]

    class Meta():
        ordering = ('-date_create',)
        verbose_name = 'коментарий'
        verbose_name_plural = 'коментарии'

    def get_absolute_url(self):
        return reverse('show_blog', kwargs={'slug':self.blog.slug})
