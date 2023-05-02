from django.urls import path
from rest_framework.routers import SimpleRouter

from ads.views.ad import AdViewSet

router = SimpleRouter()
router.register('', AdViewSet)
urlpatterns = []

urlpatterns += router.urls
