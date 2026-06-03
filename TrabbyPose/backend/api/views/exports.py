import os
from urllib.parse import unquote, urlparse

from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F, CharField, Count, Func, Value
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

        user = User.objects.first()

        if not user:
            return Response(
                {"error": "No user found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pose Post
        pose = Poses.objects.create(
            poses_fid=user,
            name_of_poses_generated=pose_name,
            configuration=pose_config
        )

        # Export Post
        export = Export.objects.create(
            export_fid=pose
        )

        return Response(
            {
                "pose_id": pose.poses_id,
                "export_id": export.export_id,
                "pose_name": pose.name_of_poses_generated,
                "pose_config": pose.configuration,
                "message": "Pose created and exported successfully"
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print("CREATE POSE ERROR:", str(e))

        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["GET"])
def get_pose_config_value(request):
    poses = Poses.objects.all().order_by("-poses_id")

    def clean(data):
        if isinstance(data, dict):
            new_data = {}
            for k, v in data.items():
                if k == "asset":
                    if v:
                        v = unquote(os.path.basename(urlparse(v.split("?")[0]).path))
                    new_data[k] = v
                else:
                    new_data[k] = clean(v)
            return new_data

        if isinstance(data, list):
            return [clean(i) for i in data]

        return data

    return Response([
        {
            "id": p.poses_id,
            "name": p.name_of_poses_generated,
            "created": getattr(p, "created_at", None),
            "config": clean(p.configuration)
        }
        for p in poses
    ])

@api_view(["GET"])
def most_used_asset(request):
    table = Poses._meta.db_table

    query = f"""
        SELECT
            split_part(
                split_part(asset::text, '?', 1),
                '/',
                array_length(string_to_array(split_part(asset::text, '?', 1), '/'), 1)
            ) AS file_name,
            COUNT(*) AS total
        FROM {table}
        CROSS JOIN LATERAL jsonb_path_query(
            configuration::jsonb,
            '$.**.asset ? (@ != null)'
        ) AS asset
        GROUP BY file_name
        ORDER BY total DESC
        LIMIT 1;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchone()

    if not row:
        return Response({"file_name": None, "total": 0})

    return Response({
        "file_name": row[0],
        "total": row[1],
    })