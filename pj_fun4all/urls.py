from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_fun4all.urls')),

    #PASSWORD RESET personalizzato
    # path(
    #     'accounts/password_reset/', 
    #     auth_views.PasswordResetView.as_view(
    #         template_name='registration/password_reset_form.html',
    #         email_template_name='registration/password_reset_email.html',  # opzionale
    #         success_url='/accounts/password_reset/done/'
    #     ), 
    #     name='password_reset'
    # ),
    #Authentication
    path('accounts/',include('django.contrib.auth.urls')),
]

urlpatterns+= static(settings.STATIC_URL,
                    document_root=settings.STATIC_ROOT)