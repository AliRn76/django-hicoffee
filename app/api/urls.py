
from django.urls import path

from app.api.views import show_all_items_view

urlpatterns = [
    path('show-all-items/', show_all_items_view)
]
