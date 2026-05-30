"""
Django REST Framework views for Puppet & Pose management APIs.

Provides endpoints for retrieving preset poses, expressions, and their
complete configuration details for frontend consumption.
"""

from typing import Optional
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncWeek

from .models import PuppetPart, PosePreset, PartConfiguration, Export, Poses, PoseSelection
from .serializers import (
    PuppetPartSerializer,
    PuppetPartHierarchicalSerializer,
    PosePresetListSerializer,
    PosePresetDetailSerializer,
    PosePresetCreateUpdateSerializer,
)


@api_view(["GET"])
def test(request: Request) -> Response:
    """
    Test endpoint to verify Django and Astro connectivity.
    
    Returns: Simple JSON message confirming API is running.
    """
    return Response({"message": "Django and Astro are connected!"})


class PosePresetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for PosePreset model.
    
    Endpoints:
        GET /api/poses/               - List all body poses
        GET /api/poses/<slug>/        - Retrieve detailed pose configuration
        GET /api/expressions/         - List all facial expressions
        GET /api/expressions/<slug>/  - Retrieve detailed expression configuration
    """

    queryset = PosePreset.objects.prefetch_related("part_configurations")
    lookup_field = "slug"

    def get_serializer_class(self):
        """
        Return appropriate serializer based on request action.
        
        - List/partial updates: use light PosePresetListSerializer
        - Retrieve: use detailed PosePresetDetailSerializer
        - Create/update: use PosePresetCreateUpdateSerializer
        """
        if self.action in ["list"]:
            return PosePresetListSerializer
        elif self.action in ["retrieve"]:
            return PosePresetDetailSerializer
        else:
            return PosePresetCreateUpdateSerializer

    def get_queryset(self):
        """
        Filter queryset by pose type based on endpoint.
        
        - /poses/ returns only body poses (is_expression=False)
        - /expressions/ returns only facial expressions (is_expression=True)
        """
        queryset = super().get_queryset()
        is_expression = self.request.path.startswith("/api/expressions/")
        return queryset.filter(is_expression=is_expression)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """
        Retrieve a single pose or expression by slug with full configuration.
        
        Returns complete pose data including all part configurations,
        positions, rotations, z-indices, and asset URLs.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except NotFound:
            pose_type = "expression" if request.path.startswith("/api/expressions/") else "pose"
            raise NotFound(
                {"detail": f"Requested {pose_type} not found."}
            )


@api_view(["GET"])
def get_poses_list(request: Request) -> Response:
    """
    Retrieve all available body poses (non-expression presets).
    
    Returns a lightweight list of poses with name, slug, and part count.
    
    Query Parameters:
        - None
    
    Returns:
        200: List of pose presets
        Example:
        [
            {
                "id": 1,
                "name": "Neutral",
                "slug": "neutral",
                "description": "Neutral standing pose...",
                "type": "body_pose",
                "is_expression": false,
                "part_count": 5,
                "created_at": "2026-05-29T..."
            },
            ...
        ]
    """
    try:
        poses = PosePreset.objects.filter(is_expression=False).all()
        serializer = PosePresetListSerializer(poses, many=True)
        return Response(
            {
                "count": len(serializer.data),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": f"Failed to retrieve poses: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_pose_detail(request: Request, slug: str) -> Response:
    """
    Retrieve detailed configuration for a specific body pose.
    
    Includes all puppet parts, their positions, rotations, z-indices,
    and asset URLs needed for rendering.
    
    Path Parameters:
        - slug: Unique identifier for the pose (e.g., 'thumbs-up')
    
    Returns:
        200: Complete pose configuration
        404: Pose not found
        
    Example Response:
        {
            "id": 1,
            "name": "Thumbs Up",
            "slug": "thumbs-up",
            "description": "Character giving a thumbs up gesture",
            "type": "body_pose",
            "is_expression": false,
            "part_configurations": [
                {
                    "id": 1,
                    "puppet_part": {
                        "id": 1,
                        "name": "Round Head",
                        "asset_url": "/assets/head_round.svg",
                        "part_type": "HEAD",
                        "part_type_display": "Head",
                        ...
                    },
                    "position_x": 200,
                    "position_y": 100,
                    "rotation": 0,
                    "z_index": 5,
                    "scale": 1.0,
                    ...
                },
                ...
            ],
            ...
        }
    """
    try:
        pose = get_object_or_404(
            PosePreset,
            slug=slug,
            is_expression=False
        )
        serializer = PosePresetDetailSerializer(pose)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": f"Failed to retrieve pose: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_expressions_list(request: Request) -> Response:
    """
    Retrieve all available facial expressions.
    
    Returns a lightweight list of expressions with name, slug, and part count.
    
    Query Parameters:
        - None
    
    Returns:
        200: List of expression presets
        Example:
        [
            {
                "id": 2,
                "name": "Happy",
                "slug": "happy",
                "description": "Happy facial expression with smile...",
                "type": "expression",
                "is_expression": true,
                "part_count": 3,
                "created_at": "2026-05-29T..."
            },
            ...
        ]
    """
    try:
        expressions = PosePreset.objects.filter(is_expression=True).all()
        serializer = PosePresetListSerializer(expressions, many=True)
        return Response(
            {
                "count": len(serializer.data),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": f"Failed to retrieve expressions: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_expression_detail(request: Request, slug: str) -> Response:
    """
    Retrieve detailed configuration for a specific facial expression.
    
    Includes all face elements, their positions, rotations, z-indices,
    and asset URLs needed for rendering.
    
    Path Parameters:
        - slug: Unique identifier for the expression (e.g., 'happy')
    
    Returns:
        200: Complete expression configuration
        404: Expression not found
        
    Example Response: Same structure as get_pose_detail but with is_expression=true
    """
    try:
        expression = get_object_or_404(
            PosePreset,
            slug=slug,
            is_expression=True
        )
        serializer = PosePresetDetailSerializer(expression)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": f"Failed to retrieve expression: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_puppet_parts(request: Request) -> Response:
    """
    Retrieve all available puppet parts/assets organized by category and subcategory.
    
    This endpoint returns a hierarchical structure matching the frontend's 
    Customization UI organization.
    
    Query Parameters:
        - category: Filter by category (Head, Limbs, Torso, Accessories)
        - format: Return format - 'hierarchical' (default) or 'flat'
        
    Returns:
        200: Puppet parts organized by category and subcategory
        
    Hierarchical Format (default):
    {
        "Head": {
            "subcategories": ["Head Position", "Face", "Eyes", ...],
            "options": {
                "Head Position": [
                    {"id": 1, "name": "head-1", "asset_url": "...", ...},
                    ...
                ],
                "Face": [...]
            }
        },
        "Limbs": {...},
        "Torso": {...},
        "Accessories": {...}
    }
    
    Flat Format:
    [
        {
            "id": 1,
            "name": "head-1",
            "asset_url": "/assets/head-1.png",
            "category": "Head",
            "subcategory": "Head Position",
            "description": "...",
            ...
        },
        ...
    ]
    """
    try:
        queryset = PuppetPart.objects.all()
        
        # Optional filtering by category
        category = request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        
        # Optional filtering by subcategory
        subcategory = request.query_params.get("subcategory")
        if subcategory:
            queryset = queryset.filter(subcategory=subcategory)
        
        # Determine response format
        response_format = request.query_params.get("format", "hierarchical")
        
        if response_format == "flat":
            # Return flat list
            serializer = PuppetPartSerializer(queryset, many=True)
            return Response(
                {
                    "count": len(serializer.data),
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            # Return hierarchical structure (default)
            serializer = PuppetPartHierarchicalSerializer()
            hierarchical_data = serializer.to_representation(queryset)
            return Response(
                hierarchical_data,
                status=status.HTTP_200_OK
            )
    except Exception as e:
        return Response(
            {"error": f"Failed to retrieve puppet parts: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
def get_puppet_parts_hierarchical(request: Request) -> Response:
    """
    Retrieve all available puppet parts organized hierarchically by category and subcategory.
    
    This is the primary endpoint for the frontend Customization page.
    
    Query Parameters:
        - category: Filter by specific category (Head, Limbs, Torso, Accessories)
        
    Returns:
        200: Hierarchical structure of puppet parts
        
    Example Response:
    {
        "Head": {
            "subcategories": ["Head Position", "Face", "Eyes", "Mouth", "Ears", "Hair", "Eyebrows"],
            "options": {
                "Head Position": [
                    {"id": 1, "name": "head-1", "asset_url": "/assets/head-1.png", "order": 0, ...},
                    {"id": 2, "name": "head-2", "asset_url": "/assets/head-2.png", "order": 1, ...},
                    ...
                ],
                "Face": [
                    {"id": 3, "name": "face-1", "asset_url": "/assets/face-1.png", "order": 0, ...},
                    ...
                ],
                ...
            }
        },
        "Limbs": {...},
        "Torso": {...},
        "Accessories": {...}
    }
    """
    try:
        queryset = PuppetPart.objects.all()
        
        # Optional filtering by category
        category = request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        
        # Use hierarchical serializer
        serializer = PuppetPartHierarchicalSerializer()
        hierarchical_data = serializer.to_representation(queryset)
        
        return Response(
            hierarchical_data,
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": f"Failed to retrieve puppet parts: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


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