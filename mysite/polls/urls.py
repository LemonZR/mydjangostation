from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('hello/', views.hello, name='hello'),
    path('touch/', views.touch, name='touch'),
    path('logout/', views.logout, name='logout'),
    path('info/', views.user_info, name='info'),
    # ex: /polls/5/
    path('<int:question_id>/', views.Detail.as_view(), name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'), Detail 类视图替代
    path('login/', views.Login.as_view(), name='login'),
    path('register/', views.Register.as_view(), name='register'),


]
