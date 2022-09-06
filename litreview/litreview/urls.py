from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from authentication.views import (login_user,
                                logout_user,
                                signup,
                                user_profile,
                                user_update,
                                user_delete,
                                follow_users)
from review import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.root_redirect_home),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', signup, name='signup'),
    path('users/<int:user_id>/', user_profile, name='user-profile'),
    path('users/<int:user_id>/update/', user_update, name='user-update'),
    path('users/<int:user_id>/delete/', user_delete, name='user-delete'),
    path('follow_users/', follow_users, name='follow-users'),
    path('home/', views.home, name='home'),
    path('int:<user_id>', views.get_user_posts, name='user-posts'),
    path('ticket/create/', views.ticket_create, name='ticket-create'),
    path('ticket/<int:ticket_id>/update/', views.ticket_update, name='ticket-update'),
    path('ticket/<int:ticket_id>/delete/', views.ticket_delete, name='ticket-delete'),
    path('review/<int:ticket_id>/create/', views.review_ticket_create, name='review-ticket-create'),
    path('review/create/', views.review_without_ticket, name='review-without-ticket'),
    path('review/<int:review_id>/update/', views.review_update, name='review-update'),
    path('review/<int:review_id>/delete/', views.review_delete, name='review-delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)