from django.urls import re_path
from inspector_app.views.order_image_views import HealthCheckView, OrderImageView

urlpatterns = [
    re_path(r'^healthcheck/', HealthCheckView.as_view()),
    re_path(r'^validate/image/v(?P<version_id>\d+)/', OrderImageView.as_view()),
]
