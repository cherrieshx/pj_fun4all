from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_fun4all.urls')),
    path('', RedirectView.as_view(url='app_fun4all/')),
    path('accounts/',include('django.contrib.auth.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns+= static(settings.STATIC_URL,
                    document_root=settings.STATIC_ROOT)