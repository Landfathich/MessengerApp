from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include  # ← добавить include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),

    path('', login_required(RedirectView.as_view(pattern_name='chat_dashboard', permanent=False))),
]
