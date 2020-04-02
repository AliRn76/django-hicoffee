
from django.urls import path

from app.api.views import show_all_items_view, add_item_view, edit_item_view, delete_item_view, show_item_view

urlpatterns = [
    path('show-all-items/', show_all_items_view),
    path('add-item/', add_item_view),
    path('edit-item/', edit_item_view),
    path('delete-item/<str:item_name>', delete_item_view),
    path('show-item/<str:item_name>', show_item_view),
]
