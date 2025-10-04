from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def delete_user(request):
    """
    Delete the currently authenticated user and redirect to homepage.
    All related data will be cleaned up by the post_delete signal.
    """
    request.user.delete()
    return redirect('home')
