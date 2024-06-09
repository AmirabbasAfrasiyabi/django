from django.http import HttpResponse


class GetGuitarists(object):
    def __init__(self, get_response):
        self.get_response = get_response
        print(get_response)
    def __call__(self, request):
        response = self.get_response(request)
        return response
    def process_request(self, request):
        x = False
        if x :
            return None
        else:
            return HttpResponse("Test Middleware")

'''
class GetGuitarists:
    def __init__(self, get_response):
        self.get_response = get_response
        print(get_response)
    def __call__(self, request):
        response = self.get_response(request)
        return response
    def process_view(self, request, dashboard, view_args, view_kwargs):
        x = True
        if x :
            print(x)
            return None
        else:
            return HttpResponse("Test Middleware")
'''
