from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'gender', 'id')
    search_fields = ('username', 'id')
    list_display_links = ('id', 'username')
    list_filter = ('username', 'gender')
    sortable_by = ('username', 'gender')


admin.site.register(Profile, ProfileAdmin)
