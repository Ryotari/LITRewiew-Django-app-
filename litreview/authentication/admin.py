from django.contrib import admin
from authentication.models import User, UserFollows

class UserAdmin(admin.ModelAdmin):
	pass

admin.site.register(User, UserAdmin)
admin.site.register(UserFollows, UserAdmin)