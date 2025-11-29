from django.urls import path

from . import views

urlpatterns = [
    path('test/', views.test_chat, name='test_chat'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # вместо LogoutView
    path('dashboard/', views.chat_dashboard, name='chat_dashboard'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('chat/start/<int:friend_id>/', views.start_chat, name='start_chat'),
    path('chat/<int:conversation_id>/', views.conversation_chat, name='conversation_chat'),
]
