from django.contrib import admin
from authentication.models import User

class UserAdmin(admin.ModelAdmin):
	pass

admin.site.register(User, UserAdmin)