# jhvar-django-utils

### 介绍

jhvar-django-utils是一个django框架下的辅助项目，基于django2.2.5开发，主要功能包括<font color="blue">动态路由授权</font>和<font color="blue">一些工具函数</font>。

同时jhvar-django-utils也是一款成长中的项目，量吸收借鉴了一些优化前端工具以及框架的设计理念和思想。如果 jhvar-django-utils 有不足地方，或者你有更好的想法，欢迎提交 ISSUE 或者 PR。

### 特性
* 基于django2.2.5，python 3.6.9
* 中间件用户角色拦截
* 基于urls静态编辑功能角色关系
* 少量代码即可完成角色权限的动态分配

### demo

setting.py
>  
>……  
>MIDDLEWARE = [  
>    'django.middleware.security.SecurityMiddleware',  
>    'django.contrib.sessions.middleware.SessionMiddleware',  
>    'jhvar.django.urls.middleware.JvRoleMiddleware',  # 保证拦截器在会话创建之后调用  
>    'corsheaders.middleware.CorsMiddleware',  
>    'django.middleware.common.CommonMiddleware',  
>    'django.middleware.csrf.CsrfViewMiddleware',  
>    'django.contrib.auth.middleware.AuthenticationMiddleware',  
>    'django.contrib.messages.middleware.MessageMiddleware',  
>    'django.middleware.clickjacking.XFrameOptionsMiddleware',  
>]  
>……  
>  
>LOGGING = {  
>    ……  
>    'loggers': {  
>        ……  
>        'jhvar.django.logger': {  # 增加拦截日志调试信息输出  
>            'handlers': ['console'],  
>            'level': DEBUG,  
>        },  
>    }  
>  
>

urls.py
>  
>……  
>from django.urls import include, path  
>from jhvar.django.urls import jv_path  
>  
>router = routers.DefaultRouter()  
>router.register('feature', Feature, basename="feature")  
>  
>app_name = 'appname'  
>permitted_roles = ['admin']  #可以在这里定义整个app的权限  
>  
>urlpatterns = [  
>    jv_path('admin', views.my_admin, name='my_admin', roles=['admin']),  #可以在这里单独定义权限，优先级高于app的权限  
>    jv_re_path(r'^api/', include(router.urls), roles='api-user'),  #可以为rest_framework限制角色  
>    path('', views.index),  
>]  
>  

views.py
>from jhvar.django.urls import grant_roles  
>……  
>def login(request):  
>    #登录校验逻辑  
>    grant_roles(request, ['admin', 'super'])  # 一句话授权
>    #完成登录  
>……  
>  


### 安装使用

>(venv)> pip install django-role-router


###### 强烈建议您使用最新版本

