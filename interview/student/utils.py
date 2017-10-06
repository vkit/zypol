from django.contrib.auth.models import User


def check_availibity(username):
    user = User.objects.filter(username=username)
    if user.exists():
        return True
    else:
        return False
