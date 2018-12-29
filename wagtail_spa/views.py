from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from wagtail.contrib.redirects.models import Redirect
from wagtail.core.models import Page

from . import settings


class RetrieveDraftMixin(RetrieveModelMixin):
    """Миксин возвращающий драфтовую версию объекта."""

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        with transaction.atomic():
            if request.GET.get('is_draft') == 'true':
                instance.get_latest_revision().publish()
                instance.refresh_from_db()

            serializer = self.get_serializer(instance)
            response = Response(serializer.data)

            if request.GET.get('is_draft') == 'true':
                transaction.set_rollback(True)
        return response


class CachedListBaseView(APIView):
    cache_key = None
    response_key = None

    def get_data(self):
        raise NotImplementedError()

    def get(self, request, *args, **kwargs):
        data = cache.get(self.cache_key)
        if data is None:
            data = self.get_data()
            cache.set(self.cache_key, data)
        return Response(data={self.response_key: data})


class RedirectsView(CachedListBaseView):
    """Список редиректов."""
    cache_key = settings.CACHE_KEY_REDIRECTS
    response_key = 'redirects'

    def get_data(self):
        redirects = []
        for obj in Redirect.objects.all():
            new_path = None
            if obj.redirect_page:
                new_path = obj.redirect_page.specific.url
            elif obj.redirect_link:
                new_path = obj.redirect_link
            redirects.append({'old': obj.old_path, 'new': new_path})
        return redirects


class URLToModelView(CachedListBaseView):
    """Соответствие урлов и моделей."""
    cache_key = settings.CACHE_KEY_URL2MODEL
    response_key = 'urls'

    def get_data(self):
        urls = []
        models = {m.pk: getattr(m.model_class(), '__name__', None) for m in ContentType.objects.all()}
        for url, ct_id in Page.objects.order_by('path').values_list('url_path', 'content_type_id'):
            urls.append({'url': url, 'model': models[ct_id]})
        return urls

