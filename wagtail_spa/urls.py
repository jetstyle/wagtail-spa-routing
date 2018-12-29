from django.urls import path
from . import views

app_name = 'wagtail_spa'
urlpatterns = [
    path('redirects', views.RedirectsView.as_view(), name='redirects'),
    path('url-to-model', views.URLToModelView.as_view(), name='url_to_model'),
]

