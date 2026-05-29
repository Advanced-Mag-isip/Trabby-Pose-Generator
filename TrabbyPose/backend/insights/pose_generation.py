from django.shortcuts import render, get_object_or_404
from .models import Poses

#view_number_of_predefined_poses
def view_number_of_predefined_poses(request, pose_id):
    pose = get_object_or_404(Poses, poses_id=pose_id)
    number_of_predefined_poses = Poses.objects.filter(
        is_predefined=True
    ).count()
    context = {
        "pose": pose,
        "number_of_predefined_poses": number_of_predefined_poses,
    }
    return render(request, "insights.html", context)

#view_number_of_customized_poses
def view_number_of_customized_poses(request, pose_id):
    pose = get_object_or_404(Poses, poses_id=pose_id)
    context = {
        "number_of_customized_poses": pose.number_of_customized_poses,
    }

    return render(request, "insights.html", context)

#view_number_of_total_poses_generated
def view_number_of_total_poses_generated(request, pose_id):
    pose = get_object_or_404(Poses, poses_id=pose_id)
    context = {
        "total_poses_generated": pose.number_of_predefined_poses + pose.number_of_customized_poses,
    }
    return render(request, "insights.html", context)

#view_pose_generation_rate_per_week
def view_pose_generation_rate_per_week(request, pose_id):
    pose = get_object_or_404(Poses, poses_id=pose_id)
    context = {
        "pose_generation_rate_per_week": pose.total_poses_generated / pose.number_of_weeks,
    }
    return render(request, "insights.html", context)

