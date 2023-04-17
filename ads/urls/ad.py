
from django.urls import path

from ads.views import AdDetailView, AdListView, AdDeleteView, AdUpdateView, AdCreateView, AdUploadImage


urlpatterns = [
    path('', AdListView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('update/<int:pk>/', AdUpdateView.as_view()),
    path('delete/<int:pk>/', AdDeleteView.as_view()),
    path('upload_image/<int:pk>/', AdUploadImage.as_view()),
]
