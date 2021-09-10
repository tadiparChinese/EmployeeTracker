from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.cache import cache


#gives count how many times the user has logged stored in cache
def login_sucess(sender, request, user, **kwargs):
    ct = cache.get('count', 0, version=user.pk)
    newcount= ct + 1
    cache.set('count', newcount, 60*60*9, version=user.pk) #maximum 9 hrs shift
    print(user.pk)