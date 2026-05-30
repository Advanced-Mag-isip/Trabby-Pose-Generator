from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import TruncMonth
from collections import defaultdict

from ...models import PoseSelection


# ---------------------------------------------------------------
# Pose Usage Data Insights
# ---------------------------------------------------------------

@api_view(["GET"])
def view_count_selection_per_pose(request):
    qs = (
        PoseSelection.objects
        .values("pose_selection_fid__name_of_poses_generated")
        .annotate(total=Count("selected_at"))
        .order_by("-total")
    )

    labels = []
    values = []

    for item in qs:
        labels.append(item["pose_selection_fid__name_of_poses_generated"])
        values.append(item["total"])

    return Response({
        "labels": labels,
        "values": values
    })


@api_view(["GET"])
def view_total_count_selection_of_poses(request):
    try:
        total = PoseSelection.objects.count()

        return Response({
            "number_of_total_count_selection_of_poses": total
        })

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=400
        )

@api_view(["GET"])
def view_top_poses_selection_count_ranking(request):
    try:
        top_poses = (
            PoseSelection.objects
            .select_related("pose_selection_fid")  # join Poses table
            .values("pose_selection_fid__name_of_poses_generated")
            .annotate(selection_count=Count("pose_selection_id"))
            .order_by("-selection_count")
        )

        labels = [
            item["pose_selection_fid__name_of_poses_generated"]
            for item in top_poses
        ]

        values = [item["selection_count"] for item in top_poses]

        return Response({
            "labels": labels,
            "values": values
        })

    except Exception as e:
        return Response({"error": str(e)}, status=400)