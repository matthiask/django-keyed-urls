from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class KeyedURL(models.Model):
    key = models.CharField(_('key'), max_length=40, unique=True)
    url = models.URLField(_('URL'), max_length=1000)

    class Meta:
        verbose_name = _('keyed URL')
        verbose_name_plural = _('keyed URLs')

    def __str__(self):
        return self.key

    def get_absolute_url(self):
        return self.url

    def get_forwarding_url(self):
        return reverse('keyed_url_forward', kwargs={'key': self.key})


@receiver(signals.post_save, sender=KeyedURL)
@receiver(signals.post_delete, sender=KeyedURL)
def _flush(instance, **kwargs):
    cache.delete_many([
        'keyed_urls:%s:%s' % (instance.key, language)
        for language, _ in settings.LANGUAGES
    ])
