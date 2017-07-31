from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Book,Group,Price,Category,Language,Author,Narrator
from .models import Currency, ProgramFormat, Publisher, Rating
from .models import UserProfile

# register each and every model
admin.site.register(Book)
admin.site.register(Group)
admin.site.register(ProgramFormat)
admin.site.register(Category)
admin.site.register(Language)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Narrator)
admin.site.register(Price)
admin.site.register(Currency)
admin.site.register(Rating)


# define inline admin descriptor for user profile model
# which acts a bit like a singleton

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'userprofile'

# Define new user admin
class UserAdmin(BaseUserAdmin):
	inlines = (UserProfileInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)