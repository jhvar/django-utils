from django.utils.deprecation import MiddlewareMixin
from django.urls import get_resolver, get_urlconf, NoReverseMatch, get_ns_resolver, URLResolver, URLPattern
from django.http.response import HttpResponseNotAllowed
import logging
from jhvar.django.urls import JvURLPattern, JvURLResolver
from .. import role_session_key, role_app_key, role_url_key
from jhvar.django.utils import safeattr
from django.urls.exceptions import Resolver404

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

        # Now, we get app url resolver
        if not isinstance(resolver, URLResolver):
            return

        path.reverse()
        view = "/".join(path)

        app_roles = safeattr(resolver.urlconf_module, role_app_key) or []
        path_roles = []
        for pattern in resolver.url_patterns:
            if isinstance(pattern, JvURLPattern) or isinstance(pattern, JvURLResolver):
                roles = safeattr(pattern, role_url_key)
                # URLResolver.resolve would raise Resolver404 exception, it lead to http 404 error directly.
                # So, we catch it and pass throught.
                try:
                    if roles and pattern.resolve(view):
                        path_roles = list(roles) if isinstance(roles, (list, tuple, set)) else [roles]
                        break
                except Resolver404:
                    pass

        if len(app_roles)==0 and len(path_roles)==0:
            return
        s_roles = request.session.get(role_session_key, None)

        if not s_roles:
            self._debug("There are no %s in session, but role required(%s|%s), access denied." % \
                        (role_session_key, ",".join(app_roles), ",".join(path_roles)))
            return HttpResponseNotAllowed(permitted_methods=[])

        if len(path_roles)>0:
            t = set(path_roles).intersection(set(s_roles))
            roles = path_roles
        else:
            t = set(app_roles).intersection(set(s_roles))
            roles = app_roles

        if len(t) == 0:
            self._debug("Session roles are '%s', mismatch urls setting(%s), access denied." % \
                        (",".join(s_roles), ",".join(roles)))
            return HttpResponseNotAllowed(permitted_methods=[])


