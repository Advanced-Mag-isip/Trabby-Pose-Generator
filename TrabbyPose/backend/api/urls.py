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
]
