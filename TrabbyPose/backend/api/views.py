# need ba inin?--------------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
# --------------------------------------------

from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncWeek

from api.models import Export
from api.models import Poses
from api.models import PoseSelection

@api_view(['GET'])
def test(request):
    return Response({"message": "Django and Astro are connected!"})



#--------------------------------------------------------------
#Views for Insights Ahead
#--------------------------------------------------------------




#---------------------------------------------------------------
#Pose Generation Data Insights
#---------------------------------------------------------------

#view_number_of_predefined_poses
def view_number_of_predefined_poses(request):
    # number_of_predefined_poses = Poses.objects.filter(
    #     is_predefined=True
    # ).count()
    number_of_predefined_poses=0

# --------------------------------------------------------------
    return JsonResponse({
        "number_of_predefined_poses": number_of_predefined_poses,
    })
# --------------------------------------------------------------


#view_number_of_customized_poses
def view_number_of_customized_poses(request):
    number_of_customized_poses = Poses.objects.count()

# --------------------------------------------------------------
    return JsonResponse({
        "number_of_customized_poses": number_of_customized_poses,
    })
# --------------------------------------------------------------

# view_number_of_total_poses_generated
def view_number_of_total_poses_generated(request):
    # number_of_predefined_poses = Poses.objects.filter(
    #     is_predefined=True
    # ).count()
    number_of_predefined_poses=0

    number_of_customized_poses = Poses.objects.count()

    total_poses_generated = number_of_predefined_poses + number_of_customized_poses

# --------------------------------------------------------------
    return JsonResponse({
        "total_poses_generated": total_poses_generated,
    })
# --------------------------------------------------------------

#view_pose_generation_rate_per_week
def view_pose_generation_rate_per_week(request):
    weekly_data = (
        Poses.objects
        .annotate(week=TruncWeek("created_at"))
        .values("week")
        .annotate(total=Count("poses_id"))
        .order_by("week")
    )

    labels = []
    data = []

    for entry in weekly_data:
        labels.append(entry["week"].strftime("%Y-%m-%d"))
        data.append(entry["total"])

    return JsonResponse({
        "labels": labels,
        "data": data
    })

#---------------------------------------------------------------
#Pose Usage Data Insights
#---------------------------------------------------------------

#view_count_selection_per_pose
def view_count_selection_per_pose(request, pose_id):
    count_selection_per_pose = PoseSelection.objects.filter(
        pose_selection_fid=pose_id
    ).count()

# --------------------------------------------------------------
    return JsonResponse({
        "number_of_count_selection_per_pose": count_selection_per_pose,
    })
# --------------------------------------------------------------

#view_total_count_selection_of_poses
def view_total_count_selection_of_poses(request):

    total_count_selection_of_poses = PoseSelection.objects.count()

# --------------------------------------------------------------
    return JsonResponse({
        "number_of_total_count_selection_of_poses": total_count_selection_of_poses,
    })
# --------------------------------------------------------------

# top_poses_selection_count_ranking

def view_top_poses_selection_count_ranking(request):
    top_poses = (
        PoseSelection.objects
        .values('pose_selection_fid')  # group by pose
        .annotate(selection_count=Count('pose_selection_id'))  # count rows
        .order_by('-selection_count')
    )

# --------------------------------------------------------------
    return JsonResponse({
        "top_poses_selection_count_ranking": list(top_poses)
    })
# --------------------------------------------------------------



#---------------------------------------------------------------
#Pose Exports Data Insights
#---------------------------------------------------------------

# View exports per pose
def view_exports_per_pose(request, pose_id):
    exports_per_pose = Export.objects.filter(
        export_fid_id=pose_id
    ).count()

# --------------------------------------------------------------
    return JsonResponse({
        "pose_id": pose_id,
        "number_exports_per_pose": exports_per_pose
    })
# --------------------------------------------------------------


# View total exports
def view_total_exports(request):
    total_exports = Export.objects.count()

# --------------------------------------------------------------
    return JsonResponse({
        "total_exports": total_exports
    })
# --------------------------------------------------------------

# View export generation per week
def view_export_generation_per_week(request):
    exports_per_week = (
        Export.objects
        .annotate(week=TruncWeek('created_at'))
        .values('week')
        .annotate(total_exports=Count('export_id'))
        .order_by('week')
    )

# --------------------------------------------------------------
    return JsonResponse({
        "exports_per_week": list(exports_per_week)
    })
# --------------------------------------------------------------