from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    """
    Delete the currently authenticated user and redirect to homepage.
    """
    request.user.delete()
    return redirect('home')

@login_required
def inbox(request):
    """
    Display unread messages for the logged-in user,
    using a raw ORM filter with select_related.
    """
    messages = (
        Message.objects
            .filter(receiver=request.user, read=False)
            .select_related('sender')
            .only('id', 'sender', 'content', 'timestamp')
    )
    return render(request, 'messaging/inbox.html', {'messages': messages})

@login_required
@require_POST
def send_message(request):
    """
    Send a new message: sets sender=request.user and uses receiver lookup.
    """
    receiver = get_object_or_404(User, pk=request.POST.get('receiver_id'))
    content = request.POST.get('content', '').strip()
    Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content
    )
    return redirect('messaging:inbox')
