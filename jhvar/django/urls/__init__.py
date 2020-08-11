from functools import partial
from django.urls.resolvers import RoutePattern, RegexPattern, URLPattern, URLResolver


class JvURLPattern(URLPattern):
    def __init__(self, pattern, callback, default_args=None, name=None, roles=None):
        super().__init__(pattern, callback, default_args=default_args, name=name)
        self.roles = roles

    def __repr__(self):
        return '<%s %s Roles:%s>' % (self.__class__.__name__, self.pattern.describe(), ",".join(self.roles) if self.roles else 'no-def')


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

