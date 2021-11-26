from django.urls.conf import include
from .views import index_view
from django.urls import path

urlpatterns = [
    path('', index_view),
    path('<path:resource>', index_view),
]
