from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="(пользователь)")
    author_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author_user.username}'

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRate=Sum('post_rating'))
        pRat = 0
        pRat += postRat.get('postRate')
        comRat = self.author_user.comment_set.all().aggregate(commentRate=Sum('comment_rating'))
        cRat = 0
        cRat += comRat.get('commentRate')
        self.author_rating = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscriber', blank=True)

    def __str__(self):
        return f'{self.category_name}'

class Subscriber(models.Model):
    subscriber_user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed_category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AT'
    TYPE_POST_CHOICES = [(NEWS, 'Новости'), (ARTICLE, 'Статья'),]

    post_type = models.CharField("Тип", max_length=2, choices=TYPE_POST_CHOICES, default=NEWS)
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Имя автора")
    post_date_time = models.DateTimeField("Дата публикации (ГГГГ-ММ-ДД)", auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory', blank=False, verbose_name="Категория", related_name='posts')
    post_title = models.CharField("Заголовок", max_length=100)
    post_text = models.TextField("Текст")
    post_rating = models.IntegerField(default=0)

    def get_absolute_url(self): # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с постом
        return f'/posts/{self.id}'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:123] + '...'

    def save_m2m(self):
        pass


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()