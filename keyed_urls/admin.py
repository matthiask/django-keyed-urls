from django.contrib import admin

from keyed_urls.models import KeyedURL


class KeyedURLAdmin(admin.ModelAdmin):
    search_fields = ('key', 'url')


admin.site.register(KeyedURL, KeyedURLAdmin)
