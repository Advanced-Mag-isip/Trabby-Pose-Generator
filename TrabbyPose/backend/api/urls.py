"""
URL routing for the Trabby Pose API.

Defines all available endpoints for:
- Pose presets (body poses)
- Expression presets (facial expressions)
- Puppet parts (asset inventory)
"""

from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    # Legacy test endpoint
    path("test/", views.test, name="test"),

    # Pose Endpoints (Body Poses)
    path(
        "poses/",
        views.get_poses_list,
        name="poses-list"
    ),
    path(
        "poses/<slug>/",
        views.get_pose_detail,
        name="pose-detail"
    ),

    # Expression Endpoints (Facial Expressions)
    path(
        "expressions/",
        views.get_expressions_list,
        name="expressions-list"
    ),
    path(
        "expressions/<slug>/",
        views.get_expression_detail,
        name="expression-detail"
    ),

    # Puppet Parts Endpoint (Asset Inventory)
    path(
        "puppet-parts/",
        views.get_puppet_parts,
        name="puppet-parts"
    ),
    path(
        "puppet-parts/hierarchical/",
        views.get_puppet_parts_hierarchical,
        name="puppet-parts-hierarchical"
    ),

    # Pose Generation Insights
    path(
        "insights/poses/predefined/",
        views.view_number_of_predefined_poses,
        name="poses-predefined-count"
    ),
    path(
        "insights/poses/customized/",
        views.view_number_of_customized_poses,
        name="poses-customized-count"
    ),
    path(
        "insights/poses/total/",
        views.view_number_of_total_poses_generated,
        name="poses-total-count"
    ),
    path(
        "insights/poses/generation-rate-per-week/",
        views.view_pose_generation_rate_per_week,
        name="poses-generation-rate-weekly"
    ),

    # Pose Usage Insights
    path(
        "insights/selections/<int:pose_id>/",
        views.view_count_selection_per_pose,
        name="pose-selections-count"
    ),
    path(
        "insights/selections/total/",
        views.view_total_count_selection_of_poses,
        name="total-selections-count"
    ),
    path(
        "insights/selections/top-ranking/",
        views.view_top_poses_selection_count_ranking,
        name="top-poses-ranking"
    ),

    # Pose Exports Insights
    path(
        "insights/exports/<int:pose_id>/",
        views.view_exports_per_pose,
        name="pose-exports-count"
    ),
    path(
        "insights/exports/total/",
        views.view_total_exports,
        name="total-exports-count"
    ),
    path(
        "insights/exports/per-week/",
        views.view_export_generation_per_week,
        name="exports-per-week"
    ),
]
