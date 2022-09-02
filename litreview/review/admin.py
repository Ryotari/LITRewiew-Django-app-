from django.contrib import admin
from .models import Review, Ticket


class ReviewAdmin(admin.ModelAdmin):
	pass

class TicketAdmin(admin.ModelAdmin):
	pass

class UserFollowsAdmin(admin.ModelAdmin):
	pass



admin.site.register(Review, ReviewAdmin)
admin.site.register(Ticket, TicketAdmin)