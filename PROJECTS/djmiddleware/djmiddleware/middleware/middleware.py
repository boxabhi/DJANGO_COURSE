


from django.http import HttpResponseForbidden
from home.models import Store

ALLOWED_IPS = ["123.45.67.89", "987.56.65.21"]


class IPBlockingMiddleware:

  
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    
    def get_client_ip(self,request):
        return (
            x_forwarded_for.split(',')[0]
            if (x_forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR'))
            else request.META.get('REMOTE_ADDR')
        )


    def __call__(self, request):
        ip = self.get_client_ip(request)
        print(ip)
        if ip in ALLOWED_IPS:
            return HttpResponseForbidden("Forbidden: IP not allowed")
        
        return self.get_response(request)
    



class CheckBMPHeader:
    
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        headers = request.headers

        if "bmp" not in headers:
            return HttpResponseForbidden("Missing : header *bmp*")
        else:
            if not Store.objects.filter(bmp_id = headers.get('bmp')).exists():
                return HttpResponseForbidden("Wrong :  *bmp*")

        
        return self.get_response(request)
    