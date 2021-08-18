from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileTbl(admin.ModelAdmin):
    list_display = ("user", "cellphone", "city", "latitude", "longitude")


    # only show data relevant to the logged in user 
    def get_queryset(self, request):
        profile_qs = super(ProfileTbl, self).get_queryset(request)
        if request.user.is_superuser:
            return profile_qs
        return profile_qs.filter(user=request.user)