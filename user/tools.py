from .models import User


def id_to_user(userID):
    try:
        user = User.objects.get(userID=userID)
    except:
        return None
    return user
