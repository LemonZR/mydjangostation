from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('drawtable/', views.drawtable_detail, name='drawtable'),
    path('update/', views.update_table_data, name='update_table_data'),
    path('search/', views.searchtable, name='searchtable'),
    path('ui/', views.update_index, name='ui'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('doonce/', views.do_once, name='do_once'),
    path('restTest/', views.RESTfulTest.as_view(), name='restTest')


]
