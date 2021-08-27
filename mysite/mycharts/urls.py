from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='test'),
    path('drawtable/', views.drawtable, name='drawtable'),
    path('update/', views.update_table_data, name='update_table_data'),
    path('search/', views.searchtable, name='searchtable'),



]
