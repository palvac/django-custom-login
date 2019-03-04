# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.decorators.cache import never_cache


class CustomAdminSite(AdminSite):
    @never_cache
    def login(self, request, extra_context=None):
        if request.method == "POST":
            password = request.POST.get("password")
            response = super(CustomAdminSite, self).login(request, extra_context=extra_context)
            if response.status_code == 302 and request.user.is_authenticated():
                if not self.is_strong_password(password):
                    request.session["force_reset_password"] = True
                    return HttpResponseRedirect(reverse("admin:password_change"))
            return response
        return super(CustomAdminSite, self).login(request, extra_context=extra_context)

    def password_change(self, request, extra_context=None):
        if request.method == "POST":
            response = super(CustomAdminSite, self).password_change(
                request, extra_context=extra_context
            )
            if response.status_code == 302 and request.user.is_authenticated():
                request.session["force_reset_password"] = False
            return response
        return super(CustomAdminSite, self).password_change(request, extra_context=extra_context)

    def is_strong_password(self, password):
        try:
            password_validation.validate_password(password)
            return True
        except ValidationError:
            return False


custom_admin_site = CustomAdminSite()


force_reset_insecure_password = CustomAdminSite().login
password_change = CustomAdminSite().password_change
