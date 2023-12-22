from urllib.parse import urlencode
from django.http import QueryDict
from django.utils.translation import gettext_lazy as _
from dj_rest_auth.views import PasswordResetConfirmView
from rest_framework.response import Response

class CustomPasswordResetConfirmView(PasswordResetConfirmView):

    def post(self, request, *args, **kwargs):
        request_data = QueryDict.dict(request.data)
        request_data['uid'] = kwargs.pop('uidb64')
        request_data['token'] = kwargs.pop('token')
        custom_request_data = QueryDict(urlencode(request_data))
        serializer = self.get_serializer(data=custom_request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': _('Password has been reset with the new password.')},
        )