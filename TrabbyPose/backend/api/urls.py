"""
URL routing for the Trabby Pose API.

Defines all available endpoints for:
- Authentication (login, logout)
- Pose presets (body poses)
- Expression presets (facial expressions)
- Puppet parts (asset inventory)

Note: User management is handled through Django admin panel at /admin/
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.auth import (
    login_user,
    logout_user,
    get_current_user,
    refresh_token,
    change_password,
)

from api.views.poses.generation import (
    view_number_of_predefined_poses,
    view_number_of_customized_poses,
    view_number_of_total_poses_generated,
    view_pose_generation_rate_per_month,
    view_top_pose_configurations,
)

from api.views.poses.usage import (
    view_count_selection_per_pose,
    view_total_count_selection_of_poses,
    view_top_poses_selection_count_ranking,
)

from api.views.exports import (
    view_exports_per_pose,
    view_total_exports,
    view_export_generation_per_month,
    create_pose,
    get_pose_config_value,
    most_used_asset,
)


# from api.views.configuration.config import (
#     test,
#     get_poses_list,
#     get_pose_detail,
#     get_expressions_list,
#     get_expression_detail,
#     get_puppet_parts,
#     get_puppet_parts_hierarchical,
# )

app_name = "api"

urlpatterns = [
    # ----------------------------------------
    # Authentication Endpoints
    # ----------------------------------------
    path('admin/', admin.site.urls),
    path("auth/login/", login_user, name="login"),
    path("auth/logout/", logout_user, name="logout"),
    path("auth/user/", get_current_user, name="current-user"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/change-password/", change_password, name="change-password"),

    # # Legacy test endpoint
    # # path("test/", views.test, name="test"),

    # # Pose Endpoints (Body Poses)
    # path("poses/", get_poses_list, name="poses-list"),
    # path("poses/<slug>/", get_pose_detail, name="pose-detail"),

    # # Expression Endpoints (Facial Expressions)
    # path("expressions/", get_expressions_list, name="expressions-list"),
    # path("expressions/<slug>/", get_expression_detail, name="expression-detail"),

    # # Puppet Parts Endpoint (Asset Inventory)
    # path("puppet-parts/", get_puppet_parts,name="puppet-parts"),
    # path("puppet-parts/hierarchical/", get_puppet_parts_hierarchical, name="puppet-parts-hierarchical"),

    # ----------------------------------------
    # Analytics Part
    # ----------------------------------------
    # Pose generation
    path("poses/predefined/", view_number_of_predefined_poses),
    path("poses/customized/", view_number_of_customized_poses),
    path("poses/totalGenerated/", view_number_of_total_poses_generated),
    path("poses/generationRate/", view_pose_generation_rate_per_month),

    # Pose usage
    path("poses/selectionPerPose/", view_count_selection_per_pose),
    path("poses/selectionTotal/", view_total_count_selection_of_poses),

    # Top Pose Configurations
    path("poses/topPoses/", view_top_poses_selection_count_ranking),
    path("poses/topConfigurations/", view_top_pose_configurations),

    # Exports
    path("exports/total/", view_total_exports),
    path("exports/pose/", view_exports_per_pose),
    path("exports/month/", view_export_generation_per_month),
    path("exports/poses/create/", create_pose),
    path("exports/pose/config/", get_pose_config_value),
    path("exports/assets/mostUsed/", most_used_asset),
]
