from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import process_data_export


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_export(request):
    """Start a background export task."""
    export_id = request.data.get("export_id")
    if not export_id:
        return Response({"error": "export_id required"}, status=400)

    result = process_data_export.delay(export_id)
    return Response({
        "task_id": result.id,
        "status": "processing",
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_task_status(request, task_id):
    """Check the status of a background task."""
    result = AsyncResult(task_id)
    response = {
        "task_id": task_id,
        "status": result.status,
        "ready": result.ready(),
    }
    if result.ready():
        response["result"] = result.result
    return Response(response)