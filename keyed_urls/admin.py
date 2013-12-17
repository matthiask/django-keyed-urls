from django.contrib import admin

from keyed_urls.models import KeyedURL


class KeyedURLAdmin(admin.ModelAdmin):
    list_display = ('key', 'url')
    ordering = ('key',)
    search_fields = ('key', 'url')


admin.site.register(KeyedURL, KeyedURLAdmin)
