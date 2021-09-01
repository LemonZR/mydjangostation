from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='test'),
    path('drawtable/', views.drawtable_detail, name='drawtable'),
    path('update/', views.update_table_data, name='update_table_data'),
    path('search/', views.searchtable, name='searchtable'),
    path('ui/', views.update_index, name='ui'),

]
