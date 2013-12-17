from modeltranslation.translator import translator, TranslationOptions

from keyed_urls.models import KeyedURL


class KeyedURLTranslationOptions(TranslationOptions):
    fields = ('url',)


translator.register(KeyedURL, KeyedURLTranslationOptions)
