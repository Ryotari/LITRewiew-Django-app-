from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import login_user, logout_user, signup
from review import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', signup, name='signup'),
    path('home/', views.home, name='home'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket-detail'),
    path('ticket/create/', views.ticket_create, name='ticket-create'),
    path('ticket/<int:ticket_id>/update/', views.ticket_update, name='ticket-update'),
    path('ticket/<int:ticket_id>/delete/', views.ticket_delete, name='ticket-delete'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)