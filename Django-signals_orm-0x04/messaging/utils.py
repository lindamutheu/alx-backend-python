# signals assignment week 6

def get_threaded_replies(message):
    replies = message.replies.select_related('sender', 'receiver').prefetch_related('replies').all()
    thread = []
    for reply in replies:
        thread.append({
            'message': reply,
            'replies': get_threaded_replies(reply)
        })
    return thread
