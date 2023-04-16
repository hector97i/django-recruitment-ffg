from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def redirect_admin(request):
    return HttpResponseRedirect('/admin/')

urlpatterns = [
    path('', redirect_admin),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/', include('api.urls')),
]
