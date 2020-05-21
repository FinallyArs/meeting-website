from django.contrib import admin
from .models import User, Profile
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext
from django.utils.translation import gettext_lazy as _




class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'gender', 'id')
    search_fields = ('username', 'id')
    list_display_links = ('id', 'username')
    list_filter = ('username', 'gender')
    sortable_by = ('username', 'gender')



admin.site.register(Profile, ProfileAdmin)
