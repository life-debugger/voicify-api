from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload_view(request):
    print(request.FILES)
    return HttpResponse("hey!")