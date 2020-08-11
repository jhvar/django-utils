import hashlib
from uuid import uuid1
import random
import string
from django.urls import reverse
from django.utils.crypto import salted_hmac
import time


def random_key():
    uid = uuid1().hex + ''.join(random.sample(string.ascii_letters + string.digits, 32))
    hash_string = salted_hmac(time.time(), uid, secret='no_one_knows').hexdigest()
    return hash_string


def md5(s):
    m = hashlib.md5()
    # 实例化md5加密方法
    m.update(s.encode())
    # 进行加密，python2可以给字符串加密，python3只能给字节加密
    result = m.hexdigest()
    return result


def full_url(request, name, kwargs=None):
    u = reverse(name, kwargs=kwargs) if kwargs else reverse(name)
    u = request.build_absolute_uri(u)
    return u
