from django.urls import path

from . import views


app_name = 'metload'
urlpatterns = [
    path('1295849198091283497812893972193748912379/', views.obsload, name='index'),
]
