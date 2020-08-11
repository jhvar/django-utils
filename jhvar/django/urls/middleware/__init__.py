from django.utils.deprecation import MiddlewareMixin
from django.urls import get_resolver, get_urlconf, NoReverseMatch, get_ns_resolver, URLResolver, URLPattern
from django.http.response import HttpResponseNotAllowed
import logging
from jhvar.django.urls import JvURLPattern


class JvRoleMiddleware(MiddlewareMixin):

    logger = logging.getLogger("jhvar.django.logger")

    def _debug(self, msg, *args, **kwargs):
        if self.logger:
            self.logger.debug(msg, *args, **kwargs)

    def process_request(self, request):
        urlconf = get_urlconf()
        resolver = get_resolver(urlconf)

        parts = request.get_full_path().split('/')
        parts.reverse()
        path = parts[:-1]
        resolved_path = []
        ns_pattern = ''
        ns_converters = {}
        while path:
            ns = path.pop()
            if ns not in resolver.app_dict:
                path.append(ns)
                break
            app_list = resolver.app_dict[ns]
            if ns not in app_list:
                ns = app_list[0]

            extra, resolver = resolver.namespace_dict[ns]
            resolved_path.append(ns)
            ns_pattern = ns_pattern + extra
            ns_converters.update(resolver.pattern.converters)

        path.reverse()
        view = "/".join(path)
        roles = None
        if isinstance(resolver, URLResolver):
            if hasattr(resolver.urlconf_module, 'permitted_roles'):
                if isinstance(resolver.urlconf_module.permitted_roles, (str, tuple, list)):
                    roles = resolver.urlconf_module.permitted_roles
            if not roles:
                for pattern in resolver.url_patterns:
                    if isinstance(pattern, URLPattern) and pattern.resolve(view):
                        if isinstance(pattern, JvURLPattern) and hasattr(pattern, 'roles'):
                            if isinstance(pattern.roles, (str, tuple, list)):
                                roles = pattern.roles
        if roles:
            if isinstance(roles, str):
                roles = [roles]
            self._debug("Url-setting requires access roles: %s" % ",".join(roles))
            if hasattr(request.session, 'roles'):
                s_roles = request.session.roles
            else:
                self._debug("There are no roles in session.roles, access denied.")
                return HttpResponseNotAllowed(permitted_methods=[])

            t = set(roles).intersection(set(s_roles))
            if len(t) == 0:
                self._debug("Session roles are '%s', do not match url-setting, access denied." % ",".join(s_roles))
                return HttpResponseNotAllowed(permitted_methods=[])

