from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_fun4all.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
]

urlpatterns+= static(settings.STATIC_URL,
                    document_root=settings.STATIC_ROOT)