from django.forms import DateInput
from django_filters import FilterSet, DateFilter, \
    CharFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post


# создаём фильтр
# venv\Lib\site-packages\django_filters\conf.py
class PostFilter(FilterSet):  # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о товарах
    post_date_time = DateFilter(lookup_expr='gt', label='Опубликовано после ', widget=DateInput(format='%d.%m.%Y', attrs={'type': 'date'}))
    post_author__author_user__username = CharFilter(lookup_expr='iexact', label='Имя автора')
    class Meta:
        model = Post
        fields = ['post_date_time', 'post_author__author_user__username']
    #    fields = { # поля, которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)
    #        'post_date_time': ['gt'],
    #         'post_title': ['icontains'], согласно заданию этот аргумент уже не нужно выводить
    #        'post_author__author_user__username': ['contains'],
    #    }