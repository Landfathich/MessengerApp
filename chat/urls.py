from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.test_chat, name='test_chat'),
]
