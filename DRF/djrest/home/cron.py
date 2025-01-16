from .models import *


def deleteRecords():
    delete_requests = DeleteRequest.objects.filter(is_done = False)
    for _request in delete_requests:
        Person.objects.filter(user = _request.user).delete()
        _request.is_done = True
        _request.save()