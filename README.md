# Установка

```
pip install wagtail-spa-routing
```

# Подключение

Добавить в `INSTALLED_APPS`:

```
'wagtail_spa.apps.WagtailSpaConfig',
```

Подключить роуты в `urls.py`:

```
path('api/wagtail-spa/', include('wagtail_spa.urls', namespace='wagtail_spa')),
```

Для добавления возможности возврата драфтового объекта, использовать `RetrieveDraftMixin`, который основан на `rest_framework.mixins.RetrieveModelMixin` и предполагает что вид возвращает объект методом `get_object`.
