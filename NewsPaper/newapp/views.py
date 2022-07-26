# print(data.__dict__) чтоб узнать все варианты
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail, \
    EmailMultiAlternatives  # импортируем классы для создания объекта письма в тесктовом и html форматах
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.template.defaultfilters import truncatechars
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from django.views.generic import ListView, UpdateView, CreateView, DetailView, \
    DeleteView  # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from django.core.paginator import Paginator

from .models import Post, Author, Category
from .filters import PostFilter  # импортируем фильтр
from .forms import PostForm  # импортируем нашу форму

from datetime import datetime


class PostsList(LoginRequiredMixin, ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-id']
    paginate_by = 3  # поставим постраничный вывод в один элемент

    # form_class = PostForm # добавляем форм класс, чтобы получать доступ к форме через метод POST

    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # получили весь контекст из класса-родителя
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        #        context['value1'] = None  # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        #        context['form'] = PostForm()
        context['is_not_authors'] = not self.request.user.groups.filter(
            name='authors').exists()  # добавили новую контекстную переменную is_not_authors
        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST-запроса
    #     if form.is_valid(): # если данные в форме ввели всё правильно, то сохраняем новый пост
    #         form.save()
    #     return super().get(request, *args, **kwargs)


class PostsSearch(ListView):
    model = Post
    template_name = 'newapp/search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


# создаём представление, в котором будут детали конкретной отдельной новости
# class PostDetail(DetailView):
#     model = Post # модель всё та же, но мы хотим получать детали конкретной отдельной новости
#     template_name = 'post.html' # название шаблона будет post.html
#     context_object_name = 'post' # название поста

# дженерик для получения деталей о товаре
class PostDetailView(DetailView):
    model = Post
    template_name = 'newapp/post_detail.html'
    context_object_name = 'post'

    #    queryset = Post.objects.all() # Если предоставлено, значение queryset заменяет значение, предоставленное для model

    # пишем функцию, чтоб ввести доп параметр is_not_subscribed для contextа.
    # Используем в шаблоне, если пользователь подписан на категорию данной новости, то кнопка не видна.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for cat in context['post'].post_category.all():
            c = Category.objects.get(id=cat.id)
            context['is_not_subscribed'] = not c.subscribers.filter(username=self.request.user.username).exists()
        return context


# создаём функцию обработчик с параметрами под регистрацию сигнала
def notify_users_post(sender, instance, created, **kwargs):
    post = Post.objects.get(id=instance.id)
    # выводим категорию для текущей новости
    for cat in post.post_category.all():
        category_for_subsc_users = Category.objects.get(id=cat.id)
        # выводим список пользователей подписанных на данную категорию
        for user in category_for_subsc_users.subscribers.all():
            # получаем наш html
            html_content = render_to_string(
                'post_dispatch.html',
                {
                    'post': instance,
                    'user_name': user.username,
                }
            )
            msg = EmailMultiAlternatives(
                subject=instance.post_title,
                # body=f'{post.post_text} \n Здравствуй, {user.username}. Новая статья в твоем любимом разделе!',
                from_email='erzhan.tleu@yandex.ru',  # здесь указываем почту, с которой будете отправлять
                to=[str(user.email)]  # емаил кому отправляем
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем

# коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
post_save.connect(notify_users_post, sender=Post)


# дженерик для создания поста. Указываем имя шаблона и класс формы.
class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'newapp/post_create.html'
    form_class = PostForm
    permission_required = ('newapp.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm
        return context

    def post(self, request, *args, **kwargs):
        new_author, created = Author.objects.get_or_create(
            author_user=self.request.user
        )
        post = Post(
            post_type=request.POST['post_type'],
            post_author=new_author,
            post_date_time=datetime.now(),
            post_title=request.POST['post_title'],
            post_text=request.POST['post_text'],
            post_rating=0,
        )
        post.save()
        post.post_category.add(int(request.POST['post_category']))
        return redirect('/')  # возврат на главную страницу новостей


# дженерик для редактирования поста
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'newapp/post_create.html'
    form_class = PostForm
    permission_required = ('newapp.change_post',)

    # метод get_object мы используем вместо queryset, чтобы получить информацию о посте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления поста
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'newapp/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'
    permission_required = ('newapp.delete_post',)


# подписываем пользователя на категорию новостей
@login_required
def subscribe_me(request, pk=0):
    post = Post.objects.get(id=pk)
    for cat in post.post_category.all():
        c = Category.objects.get(id=cat.id)
        if not c.subscribers.filter(username=request.user.username).exists():
            c.subscribers.add(request.user)
    return redirect('/')
