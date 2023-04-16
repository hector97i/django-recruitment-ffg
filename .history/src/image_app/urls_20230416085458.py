from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView
from django.http import HttpResponseRedirect

def redirect_admin(request):
    return HttpResponseRedirect('/admin/')

urlpatterns = [
    path('', redirect_admin),
    path('admin/', admin.site.urls),
    path('api/swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
