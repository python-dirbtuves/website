from django.middleware.locale import LocaleMiddleware
from django.utils import translation


class UserProfileLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        if (hasattr(request.user, 'userprofile') and
                request.user.userprofile and
                request.user.userprofile.language):
            language = request.user.userprofile.language
            translation.activate(language)
            request.LANGUAGE_CODE = language
        else:
            super(UserProfileLocaleMiddleware, self).process_request(request)
