import re

from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.utils.deprecation import MiddlewareMixin


class ForceResetPasswordMiddleware(MiddlewareMixin):
    def process_request(self, request):

        if (request.user.is_authenticated()
            and re.match(r"^/admin/?", request.path)
            and (request.session.get("force_reset_password", False))
            and not re.match(r"/admin/password_change|/admin/logout|/admin/password_change/done", request.path)
            ):
            print("redirecting user to change their password")
            print(request.session.get("force_reset_password"))
            return HttpResponseRedirect(reverse("admin:password_change"))
