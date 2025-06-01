from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from inspector_app.managers.health_check_manager import HealthCheckManager
from inspector_app.managers.order_image_manager import OrderImageManager


class HealthCheckView(APIView):
    """
    Get server status
    """
    def get(self, request, version_id):
        response = HealthCheckManager().get_server_status()
        return Response({
            "success": True,
            "message": response
        }, status.HTTP_200_OK)


class OrderImageView(APIView):
    """
    View to classify image orders
    """
    def post(self, request, version_id):
        order_id = request.data.get("order_id")
        image_file = request.FILES.getlist("order_image")
        response = OrderImageManager().inspect_and_validate_image(order_id, image_file)
        return Response({
            "success": True,
            "data": response
        }, status.HTTP_200_OK)
