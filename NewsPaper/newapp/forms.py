from django.forms import ModelForm, CheckboxSelectMultiple
from .models import Post

# импортировали класс формы, который предоставляет allauth, а также модель групп
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

# импортировать редирект и декоратор проверки аутентификации для добавления в группу Authors
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Создаём модельную форму
class PostForm(ModelForm):

    # в класс мета, пишем модель, по которой будет строиться форма и перечисляем нужные нам поля.
    class Meta:
        model = Post
        fields = ['post_type', 'post_category', 'post_title', 'post_text']
        widgets = {
             'postCategory': CheckboxSelectMultiple(),
        }

# Кастомизируем форму регистрации SignupForm, которую предоставляет пакет allauth
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request) # вызываем этот же метод класса-родителя, чтобы необходимые проверки и сохранение в модель User были выполнены
        basic_group = Group.objects.get(name='common') # получаем объект модели группы common
        basic_group.user_set.add(user) # через атрибут user_set, возвращающий список всех пользователей этой группы, мы добавляем нового пользователя в эту группу
        return user # Обязательным требованием метода save() является возвращение объекта модели User по итогу выполнения функции

# пишем функцию-представление для добавления в группу Authors
@login_required
def upgrade_me(request):
    user = request.user # получили объект текущего пользователя из переменной запроса
    authors_group = Group.objects.get(name='authors') # Вытащили authors-группу из модели Group
    if not request.user.groups.filter(name='authors').exists(): # проверяем, находится ли пользователь в этой группе (вдруг кто-то решил перейти по этому URL, уже имея группу Authors)
        authors_group.user_set.add(user) # если user всё-таки ещё не в ней — то добавляем.
    return redirect('/') # перенаправляем пользователя на корневую страницу, используя метод redirect