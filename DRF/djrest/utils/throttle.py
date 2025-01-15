from rest_framework.throttling import BaseThrottle



class CustomThrottle(BaseThrottle):
    def allow_request(self, request, view):
        if request.META['REMOTE_ADDR'] == '127.0.0.1':
            return True

        return True


