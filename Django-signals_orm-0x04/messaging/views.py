from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Message
from .utils import get_threaded_replies

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