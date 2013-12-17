from django.contrib import admin

from keyed_urls.models import KeyedURL


class KeyedURLAdmin(admin.ModelAdmin):
    ordering = ('key',)
    search_fields = ('key', 'url')


admin.site.register(KeyedURL, KeyedURLAdmin)
