from django.contrib import admin
from django.urls import path

from authentication import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_page, name='login-page')
]
