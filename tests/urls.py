"""URL configuration for tests."""

from django.contrib import admin
from django.urls import path

from tests.demo import views as demo_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("demo/single/", demo_views.single_message, name="demo-single"),
    path("demo/multiple/", demo_views.multiple_messages, name="demo-multiple"),
    path("demo/multiple-places/", demo_views.message_multiple_places, name="demo-multiple-places"),
]
