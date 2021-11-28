from django.urls import path, include

urlpatterns = [
    path('api/', include("api_gate.urls")),
    path('', include("main.urls")),
]
