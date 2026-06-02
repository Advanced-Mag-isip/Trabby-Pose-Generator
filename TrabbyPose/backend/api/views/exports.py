from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncMonth
from collections import defaultdict
from rest_framework import status


from ..models import User, Poses, Export

# ---------------------------------------------------------------
# Pose Exports Data Insights
# ---------------------------------------------------------------

@api_view(["GET"])
def view_exports_per_pose(request):
    qs = (
        Export.objects
        .values("export_fid__name_of_poses_generated")
        .annotate(total=Count("export_id"))
        .order_by("-total")
    )

    labels = [item["export_fid__name_of_poses_generated"] for item in qs]
    values = [item["total"] for item in qs]

    return Response({
        "labels": labels,
        "values": values
    })


@api_view(["GET"])
def view_total_exports(request):
    return Response({
        "total_exports": Export.objects.count()
    })


@api_view(["GET"])
def view_export_generation_per_month(request):
    exports_per_month = (
        Export.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total_exports=Count("export_id"))
        .order_by("month")
    )

    # Map month number -> count
    month_map = defaultdict(int)

    for item in exports_per_month:
        if item["month"]:
            month_index = item["month"].month  # 1–12
            month_map[month_index] = item["total_exports"]

    # Fixed labels Jan–Dec
    labels = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    # Fill missing months with 0
    values = [month_map[i] for i in range(1, 13)]

    return Response({
        "labels": labels,
        "values": values
    })


@api_view(["POST"])
def create_pose(request):
    try:
        pose_name = request.data.get("pose_name")
        pose_config = request.data.get("pose")

        if not pose_name:
            return Response(
                {"error": "pose_name is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # TEMPORARY
        user = User.objects.first()

        if not user:
            return Response(
                {"error": "No user found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        pose = Poses.objects.create(
            poses_fid=user,
            name_of_poses_generated=pose_name,
            configuration=pose_config
        )

        return Response(
            {
                "pose_id": pose.poses_id,
                "pose_name": pose.name_of_poses_generated,
                "message": "Pose created successfully"
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print("CREATE POSE ERROR:", str(e))

        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )