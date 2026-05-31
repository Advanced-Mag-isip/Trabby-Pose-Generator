from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncMonth
from collections import defaultdict

from ...models import Poses

# ---------------------------------------------------------------
# Pose Generation Data Insights
# ---------------------------------------------------------------

@api_view(["GET"])
def view_number_of_predefined_poses(request):

    number_of_predefined_poses = 0

    return Response({
        "number_of_predefined_poses": number_of_predefined_poses,
    })


@api_view(["GET"])
def view_number_of_customized_poses(request):
    return Response({
        "number_of_customized_poses": Poses.objects.count(),
    })


@api_view(["GET"])
def view_number_of_total_poses_generated(request):
    # Replace with actual query if you have an is_predefined field
    number_of_predefined_poses = 0
    number_of_customized_poses = Poses.objects.count()

    return Response({
        "total_poses_generated":
            number_of_predefined_poses + number_of_customized_poses,
    })

@api_view(["GET"])
def view_pose_generation_rate_per_month(request):
    data = (
        Poses.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("poses_id"))
        .order_by("month")
    )

    # map DB results -> {month_index: count}
    month_map = {}
    for entry in data:
        if entry["month"]:
            month_index = entry["month"].month  # 1–12
            month_map[month_index] = entry["total"]

    # fixed labels
    labels = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    # fill missing months with 0
    values = [
        month_map.get(i, 0)
        for i in range(1, 13)
    ]

    return Response({
        "labels": labels,
        "values": values
    })