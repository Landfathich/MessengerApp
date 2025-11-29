from django.contrib import admin
from django.urls import path, include  # ← добавить include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
]
