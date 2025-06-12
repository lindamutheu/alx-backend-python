from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Message
from django.db.models import Prefetch
from .utils import get_threaded_replies
from django.views.decorators.cache import cache_page

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('account_deleted')  # or home page
    return render(request, 'account/confirm_delete.html')


#task 6 threaded conversations
def message_detail(request, message_id):
    root_message = get_object_or_404(Message, pk=message_id)
    if root_message.parent_message:
        # shoul be at the top the top of a thread
        root_message = root_message.parent_message

    thread = get_threaded_replies(root_message)
    return render(request, 'messaging/message_detail.html', {
        'root': root_message,
        'thread': thread
    })

# Recursive function to fetch replies using ORM
def get_threaded_replies(message):
    replies = (
        message.replies
        .select_related('sender', 'receiver')
        .prefetch_related('replies')
        .all()
    )
    return [
        {
            'message': reply,
            'replies': get_threaded_replies(reply)
        }
        for reply in replies
    ]

@login_required
def message_detail(request, message_id):
    # Root message with select_related and prefetch_related
    root_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver', 'parent_message')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        ),
        id=message_id
    )

    # If viewing a reply, get the thread's root
    if root_message.parent_message:
        root_message = root_message.parent_message

    thread = get_threaded_replies(root_message)

    return render(request, 'messaging/message_detail.html', {
        'root': root_message,
        'thread': thread,
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver_id = request.POST.get('receiver_id')
        parent_id = request.POST.get('parent_id')

        if content and receiver_id:
            receiver = get_object_or_404(User, id=receiver_id)
            parent = Message.objects.filter(id=parent_id).first() if parent_id else None

            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content,
                parent_message=parent
            )
            return redirect('inbox')  # or wherever your redirect goes

    return render(request, 'messaging/send_message.html')

@login_required
def unread_inbox(request):
    # the custom manager method
    unread_messages = Message.unread.unread_for_user(request.user)

    #  .only() is already applied inside the manager, but shown here explicitly if needed:
    # unread_messages = unread_messages.only('id', 'sender', 'content', 'timestamp')

    return render(request, 'messaging/unread_inbox.html', {
        'unread_messages': unread_messages
    })


# Cache this view for 60 seconds
@cache_page(60)
@login_required
def conversation_view(request, user_id):
    messages = Message.objects.filter(
        sender=request.user, receiver__id=user_id
    ).union(
        Message.objects.filter(sender__id=user_id, receiver=request.user)
    ).select_related('sender', 'receiver').order_by('timestamp')

    return render(request, 'messaging/conversation.html', {
        'messages': messages
    })