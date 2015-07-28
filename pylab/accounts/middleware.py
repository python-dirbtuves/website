from django.middleware.locale import LocaleMiddleware
from django.utils import translation


class UserProfileLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        if (hasattr(request.user, 'profile') and
                request.user.profile and
                request.user.profile.language):
            language = request.user.profile.language
            translation.activate(language)
            request.LANGUAGE_CODE = language
        else:
            super(UserProfileLocaleMiddleware, self).process_request(request)
