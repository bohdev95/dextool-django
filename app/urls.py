
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_project', views.add_project, name='add_project'),
    path('get_project', views.get_project, name='get_project')
]
