from django.contrib import admin

from .forms import SignUpForm
from .models import SignUp, Hobby

# class SignUpAdmin(admin.ModelAdmin):
#     list_display = ["__unicode__", "timestamp", "updated"]
#     form = SignUpForm
# #    class Meta:
# #	model = SignUp

# class HobbyInLine(admin.StackedInline):
#     model = Hobby
#     extra = 3 

# admin.site.register(SignUp, SignUpAdmin)
# admin.site.register(Hobby)

class HobbiesInline(admin.StackedInline):
    model = Hobby
    extra = 3

class SignUpAdmin(admin.ModelAdmin):
    inlines = [HobbiesInline]

admin.site.register(SignUp, SignUpAdmin)
