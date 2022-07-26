from django.urls import path, include
from .views import PostsList, PostsSearch, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, \
    subscribe_me  # импортируем наше представление
from .forms import upgrade_me # Импортируем функцию-представление из формы

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', PostsList.as_view()),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
#    path('<int:pk>', PostDetail.as_view()),  pk — это первичный ключ новости, которая будет выводиться у нас в шаблон
    path('search/', PostsSearch.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'), # Ссылка на детали поста
    path('create/', PostCreateView.as_view(), name='post_create'), # Ссылка на создание поста
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'), # Ссылка на редактирование поста
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'), # Ссылка на удаление поста
    path('upgrade/', upgrade_me, name = 'upgrade'), # связываем кнопку "Хочу стать автором!" с функцией "upgrade_me", добавляя соответствующую строку в файл конфигурации URL
    path('posts/accounts/', include('allauth.urls')), # Logout из гугл аккаунта проходит через posts/accounts/logout/, поэтому этот путь установлен в url приложения, а не проекта.
    path('<int:pk>/subscribe/', subscribe_me, name = 'subscribe')
]