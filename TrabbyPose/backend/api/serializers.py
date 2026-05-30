"""
Django REST Framework Serializers for Puppet & Pose management.

This module provides serializers for converting model instances to/from JSON,
with support for nested relationships and comprehensive validation.
"""

from typing import Any, Dict
from rest_framework import serializers
from django.db.models import QuerySet
from .models import PuppetPart, PosePreset, PartConfiguration


class PuppetPartSerializer(serializers.ModelSerializer):
    """
    Serializer for PuppetPart model.
    
    Provides a flat representation of a puppet asset option.
    """

    class Meta:
        model = PuppetPart
        fields = [
            "id",
            "name",
            "asset_url",
            "category",
            "subcategory",
            "description",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PuppetPartHierarchicalSerializer(serializers.Serializer):
    """
    Hierarchical serializer that organizes puppet parts into the structure
    expected by the frontend (Category → Subcategory → Options).
    
    Returns data in the format:
    {
        "Head": {
            "subcategories": ["Head Position", "Face", "Eyes", ...],
            "options": {
                "Head Position": [
                    {"id": 1, "name": "head-1", "asset_url": "...", ...},
                    ...
                ],
                "Face": [...],
                ...
            }
        },
        "Limbs": {...},
        "Torso": {...},
        "Accessories": {...}
    }
    """

    def to_representation(self, data: QuerySet) -> Dict[str, Any]:
        """
        Transform flat queryset into hierarchical structure organized by
        category and subcategory.
        """
        # Fetch all parts from the queryset
        all_parts = list(data) if isinstance(data, QuerySet) else data
        
        # Build the hierarchical structure
        hierarchy = {}
        
        for part in all_parts:
            category = part.category
            subcategory = part.subcategory
            
            # Initialize category if not present
            if category not in hierarchy:
                hierarchy[category] = {
                    "subcategories": [],
                    "options": {}
                }
            
            # Initialize subcategory if not present
            if subcategory not in hierarchy[category]["options"]:
                hierarchy[category]["subcategories"].append(subcategory)
                hierarchy[category]["options"][subcategory] = []
            
            # Add the part to the options
            hierarchy[category]["options"][subcategory].append({
                "id": part.id,
                "name": part.name,
                "asset_url": part.asset_url,
                "description": part.description,
                "order": part.order,
            })
        
        # Sort subcategories and options by order
        for category in hierarchy:
            hierarchy[category]["subcategories"].sort()
            for subcategory in hierarchy[category]["options"]:
                hierarchy[category]["options"][subcategory].sort(
                    key=lambda x: x["order"]
                )
        
        return hierarchy


class PartConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer for PartConfiguration model.
    
    Provides detailed positioning, rotation, and layering information
    for a puppet part within a specific pose preset.
    """

    puppet_part = PuppetPartSerializer(read_only=True)
    puppet_part_id = serializers.PrimaryKeyRelatedField(
        queryset=PuppetPart.objects.all(),
        write_only=True,
        source="puppet_part",
        help_text="ID of the PuppetPart to configure"
    )

    class Meta:
        model = PartConfiguration
        fields = [
            "id",
            "puppet_part",
            "puppet_part_id",
            "position_x",
            "position_y",
            "rotation",
            "z_index",
            "scale",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_rotation(self, value: float) -> float:
        """Ensure rotation is within valid range (0-360 degrees)."""
        if not 0 <= value <= 360:
            raise serializers.ValidationError(
                "Rotation must be between 0 and 360 degrees."
            )
        return value

    def validate_scale(self, value: float) -> float:
        """Ensure scale is positive."""
        if value <= 0:
            raise serializers.ValidationError("Scale must be a positive number.")
        return value


class PosePresetDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for PosePreset model, including all part configurations.
    
    Used when fetching a single pose to provide complete layout information.
    """

    part_configurations = PartConfigurationSerializer(
        many=True,
        read_only=True,
        help_text="List of part configurations that make up this pose"
    )
    type = serializers.SerializerMethodField(
        help_text="Pose type (body_pose or expression)"
    )

    class Meta:
        model = PosePreset
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "type",
            "is_expression",
            "part_configurations",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_type(self, obj: PosePreset) -> str:
        """Return human-readable pose type."""
        return "expression" if obj.is_expression else "body_pose"


class PosePresetListSerializer(serializers.ModelSerializer):
    """
    Summary serializer for PosePreset model.
    
    Used when listing poses (lighter payload without full part configs).
    """

    type = serializers.SerializerMethodField(
        help_text="Pose type (body_pose or expression)"
    )
    part_count = serializers.SerializerMethodField(
        help_text="Number of parts in this pose"
    )

    class Meta:
        model = PosePreset
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "type",
            "is_expression",
            "part_count",
            "created_at",
        ]
        read_only_fields = fields

    def get_type(self, obj: PosePreset) -> str:
        """Return human-readable pose type."""
        return "expression" if obj.is_expression else "body_pose"

    def get_part_count(self, obj: PosePreset) -> int:
        """Return number of parts in this pose."""
        return obj.part_configurations.count()


class PosePresetCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating PosePreset models.
    
    Supports nested creation/update of part configurations.
    """

    part_configurations = PartConfigurationSerializer(
        many=True,
        required=False,
        help_text="Part configurations to create/update with this pose"
    )

    class Meta:
        model = PosePreset
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "is_expression",
            "part_configurations",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data: Dict[str, Any]) -> PosePreset:
        """Create a new PosePreset with nested part configurations."""
        part_configs_data = validated_data.pop("part_configurations", [])
        pose_preset = PosePreset.objects.create(**validated_data)

        for config_data in part_configs_data:
            PartConfiguration.objects.create(
                pose_preset=pose_preset,
                **config_data
            )

        return pose_preset

    def update(
        self,
        instance: PosePreset,
        validated_data: Dict[str, Any]
    ) -> PosePreset:
        """Update an existing PosePreset with nested part configurations."""
        part_configs_data = validated_data.pop("part_configurations", None)

        # Update base fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update part configurations if provided
        if part_configs_data is not None:
            instance.part_configurations.all().delete()
            for config_data in part_configs_data:
                PartConfiguration.objects.create(
                    pose_preset=instance,
                    **config_data
                )

        return instance
