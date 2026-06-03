import os
from urllib.parse import urlparse

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
    poses = Poses.objects.all()

    seen_signatures = set()

    for p in poses:
        config = p.configuration

        assets = []

        def extract_assets(data):
            if isinstance(data, dict):
                for k, v in data.items():
                    if k == "asset" and v:
                        filename = os.path.basename(urlparse(v.split("?")[0]).path)
                        assets.append(filename)
                    else:
                        extract_assets(v)

            elif isinstance(data, list):
                for item in data:
                    extract_assets(item)

        extract_assets(config)

        signature = tuple(sorted(assets))

        seen_signatures.add(signature)

    return Response({
        "total_poses_generated": len(seen_signatures)
    })

@api_view(["GET"])
def view_pose_generation_rate_per_month(request):
    poses = Poses.objects.all().order_by("created_at")

    monthly_signatures = defaultdict(set)

    for p in poses:
        config = p.configuration

        assets = []

        def extract_assets(data):
            if isinstance(data, dict):
                for k, v in data.items():
                    if k == "asset" and v:
                        filename = os.path.basename(
                            urlparse(v.split("?")[0]).path
                        )
                        assets.append(filename)
                    else:
                        extract_assets(v)

            elif isinstance(data, list):
                for item in data:
                    extract_assets(item)

        extract_assets(config)

        signature = tuple(sorted(assets))

        month_index = p.created_at.month
        monthly_signatures[month_index].add(signature)

    labels = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    values = [
        len(monthly_signatures.get(i, set()))
        for i in range(1, 13)
    ]

    return Response({
        "labels": labels,
        "values": values
    })

@api_view(["GET"])
def view_top_pose_configurations(request):
    poses = Poses.objects.all()

    signature_count = defaultdict(int)

    for p in poses:
        config = p.configuration

        assets = []

        def extract_assets(data):
            if isinstance(data, dict):
                for k, v in data.items():
                    if k == "asset" and v:
                        filename = os.path.basename(urlparse(v.split("?")[0]).path)
                        assets.append(filename)
                    else:
                        extract_assets(v)

            elif isinstance(data, list):
                for item in data:
                    extract_assets(item)

        extract_assets(config)

        signature = " + ".join(sorted(assets))
        signature_count[signature] += 1

    # sort by most common
    sorted_data = sorted(
        signature_count.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # top 10 only (important for charts)
    top_data = sorted_data[:10]

    return Response({
        "labels": [item[0] for item in top_data],
        "values": [item[1] for item in top_data]
    })