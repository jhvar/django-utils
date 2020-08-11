from functools import partial
from django.urls.resolvers import RoutePattern, RegexPattern, URLPattern, URLResolver
import logging

role_session_key = 'roles'
role_app_key = 'permitted_roles'
role_url_key = 'roles'

class JvURLPattern(URLPattern):
    def __init__(self, pattern, callback, default_args=None, name=None, roles=None):
        super().__init__(pattern, callback, default_args=default_args, name=name)
        self.roles = roles

    def __repr__(self):
        return '<%s %s Roles:%s>' % (self.__class__.__name__, self.pattern.describe(), ",".join(self.roles) if self.roles else 'no-def')


def grant_roles(request, roles):
    if isinstance(roles, str):
        roles = [roles]
    if isinstance(roles, tuple):
        roles = list(roles)
    if not isinstance(roles, list):
        raise Exception('roles must be string, tuple or list')
    if request and hasattr(request, 'session'):
        if request.session.exists(role_session_key):
            s_roles = request.session[role_session_key]
            s_roles = list(set(s_roles).union(set(roles)))
            request.session[role_session_key] = s_roles
        else:
            request.session[role_session_key] = roles
        logger = logging.getLogger("jhvar.django.logger")
        logger.debug("Current session roles are %s" % ",".join(request.session[role_session_key]))


def _jhvar_path(route, view, kwargs=None, name=None, Pattern=None, roles=None):
    if isinstance(view, (list, tuple)):
        # For include(...) processing.
        pattern = Pattern(route, is_endpoint=False)
        urlconf_module, app_name, namespace = view
        return URLResolver(
            pattern,
            urlconf_module,
            kwargs,
            app_name=app_name,
            namespace=namespace,
        )
    elif callable(view):
        pattern = Pattern(route, name=name, is_endpoint=True)
        return JvURLPattern(pattern, view, kwargs, name, roles)
    else:
        raise TypeError('view must be a callable or a list/tuple in the case of include().')


jv_path = partial(_jhvar_path, Pattern=RoutePattern)
jv_re_path = partial(_jhvar_path, Pattern=RegexPattern)

