# Create your views here.
from django.shortcuts import render


def test_chat(request):
    return render(request, 'chat/test_chat.html')
