def test_chat(request):
    return render(request, 'chat/test_chat.html')


from django.contrib.auth.decorators import login_required

from .models import Conversation, Message


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'chat/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('chat_dashboard')
    else:
        form = LoginForm()
    return render(request, 'chat/login.html', {'form': form})


@login_required
def chat_dashboard(request):
    # Получаем всех друзей пользователя
    friendships_as_user1 = Friendship.objects.filter(user1=request.user)
    friendships_as_user2 = Friendship.objects.filter(user2=request.user)

    # Собираем всех друзей в один список
    friends = []
    for friendship in friendships_as_user1:
        friends.append({
            'user': friendship.user2,
            'friendship': friendship
        })
    for friendship in friendships_as_user2:
        friends.append({
            'user': friendship.user1,
            'friendship': friendship
        })

    return render(request, 'chat/dashboard.html', {
        'user': request.user,
        'friends': friends
    })


from django.shortcuts import get_object_or_404


@login_required
def conversation_chat(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.user not in conversation.participants.all():
        return redirect('chat_dashboard')

    # ЗАГРУЖАЕМ ИСТОРИЮ СООБЩЕНИЙ
    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

    other_participants = conversation.participants.exclude(id=request.user.id)
    other_user = other_participants.first() if not conversation.is_group else None

    return render(request, 'chat/conversation.html', {
        'conversation': conversation,
        'other_user': other_user,
        'user': request.user,
        'messages': messages  # ← передаем сообщения в шаблон
    })


@login_required
def start_chat(request, friend_id):
    friend = get_object_or_404(CustomUser, id=friend_id)

    # Ищем существующий чат или создаем новый
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=friend
    ).filter(
        is_group=False
    ).first()

    if not conversation:
        conversation = Conversation.objects.create(is_group=False)
        conversation.participants.add(request.user, friend)

    return redirect('conversation_chat', conversation_id=conversation.id)


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from .models import CustomUser, Friendship


@login_required
def add_friend(request):
    if request.method == 'POST':
        friend_code = request.POST.get('friend_code')

        try:
            # Ищем пользователя по коду
            friend_user = CustomUser.objects.get(friend_code=friend_code)

            # Проверяем что не добавляем себя
            if friend_user == request.user:
                messages.error(request, "You cannot add yourself as a friend")
            else:
                # Создаем дружбу (проверяем что не дублируем)
                friendship, created = Friendship.objects.get_or_create(
                    user1=request.user,
                    user2=friend_user
                )
                if created:
                    messages.success(request, f"Successfully added {friend_user.username} as friend!")
                else:
                    messages.info(request, f"You are already friends with {friend_user.username}")

        except CustomUser.DoesNotExist:
            messages.error(request, "User with this friend code not found")

    return redirect('chat_dashboard')
