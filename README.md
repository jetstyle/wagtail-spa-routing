# Подключение

Добавить в `INSTALLED_APPS`:

```
'wagtail_spa.apps.WagtailSpaConfig',
```

Подключить роуты в `urls.py`:

```
path('api/wagtail-spa/', include('wagtail_spa.urls', namespace='wagtail_spa')),
```

