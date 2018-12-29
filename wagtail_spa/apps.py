from django.apps import AppConfig, apps
from django.db.models import signals
from django.core.cache import cache

from . import settings


class WagtailSpaConfig(AppConfig):
    name = 'wagtail_spa'

    def ready(self):
        signals.post_save.connect(page_cache)
        signals.post_delete.connect(page_cache)

        redirect_model = apps.get_model('wagtailredirects', 'Redirect')
        signals.post_save.connect(redirect_cache, sender=redirect_model)
        signals.post_delete.connect(redirect_cache, sender=redirect_model)


def page_cache(sender, instance, **kwargs):
    """Инвалидация кэша ручки URLToModelView при изменении / удалении страниц."""
    page_model = apps.get_model('wagtailcore', 'Page')
    if isinstance(instance, page_model):
        cache.delete(settings.CACHE_KEY_URL2MODEL)


def redirect_cache(sender, instance, **kwargs):
    """Инвалидация кэша ручки RedirectsView при изменении / удалении редиректов."""
    cache.delete(settings.CACHE_KEY_REDIRECTS)

