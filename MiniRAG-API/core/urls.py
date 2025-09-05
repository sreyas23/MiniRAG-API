from django.urls import path
from . import views

urlpatterns = [
    path('', views.RootView.as_view(), name='api-root'),
    path('ingest/', views.IngestView.as_view(), name='ingest'),
    path('query/', views.QueryView.as_view(), name='query'),
    path('reset/', views.ResetView.as_view(), name='reset'),
]
