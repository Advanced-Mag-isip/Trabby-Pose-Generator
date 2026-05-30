"""
Django Admin configuration for Puppet & Pose management models.

Provides a user-friendly interface for managing puppet parts, pose presets,
and their configurations in the Django admin panel.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    User,
    Poses,
    PoseSelection,
    Export,
    PuppetPart,
    PosePreset,
    PartConfiguration,
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model."""
    list_display = ("user_name", "email_address", "first_name", "last_name", "is_permitted")
    list_filter = ("is_permitted", "created_at")
    search_fields = ("user_name", "email_address", "first_name", "last_name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Poses)
class PosesAdmin(admin.ModelAdmin):
    """Admin interface for Poses model."""
    list_display = ("name_of_poses_generated", "poses_fid", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name_of_poses_generated",)
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Pose Information", {
            "fields": ("poses_fid", "name_of_poses_generated")
        }),
        ("Configuration", {
            "fields": ("configuration",),
            "classes": ("collapse",)
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )


@admin.register(PoseSelection)
class PoseSelectionAdmin(admin.ModelAdmin):
    """Admin interface for PoseSelection model."""
    list_display = ("pose_selection_id", "pose_selection_fid", "selected_at")
    list_filter = ("selected_at",)
    readonly_fields = ("selected_at",)


@admin.register(Export)
class ExportAdmin(admin.ModelAdmin):
    """Admin interface for Export model."""
    list_display = ("export_id", "export_fid", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

@admin.register(PuppetPart)
class PuppetPartAdmin(admin.ModelAdmin):
    """Admin interface for PuppetPart model."""
    list_display = (
        "name",
        "part_type_colored",
        "asset_preview",
        "created_at"
    )
    list_filter = ("part_type", "created_at")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at", "asset_preview")
    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "part_type", "description")
        }),
        ("Asset", {
            "fields": ("asset_url", "asset_preview")
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def part_type_colored(self, obj: PuppetPart) -> str:
        """Display part type with color coding."""
        colors = {
            "HEAD": "#FF6B6B",
            "TORSO": "#4ECDC4",
            "LIMB": "#45B7D1",
            "FACE": "#FFA07A",
            "EXTRA": "#98D8C8",
        }
        color = colors.get(obj.part_type, "#999")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px;">{}</span>',
            color,
            obj.get_part_type_display()
        )
    part_type_colored.short_description = "Part Type"

    def asset_preview(self, obj: PuppetPart) -> str:
        """Display a preview link for the asset."""
        if obj.asset_url:
            return format_html(
                '<a href="{}" target="_blank">View Asset →</a>',
                obj.asset_url
            )
        return "No asset URL"
    asset_preview.short_description = "Asset Preview"


class PartConfigurationInline(admin.TabularInline):
    """Inline admin for PartConfiguration within PosePreset."""
    model = PartConfiguration
    extra = 1
    fields = ("puppet_part", "position_x", "position_y", "rotation", "z_index", "scale")
    readonly_fields = ("created_at", "updated_at")


@admin.register(PosePreset)
class PosePresetAdmin(admin.ModelAdmin):
    """Admin interface for PosePreset model."""
    list_display = (
        "name",
        "slug",
        "type_badge",
        "part_count",
        "created_at"
    )
    list_filter = ("is_expression", "created_at")
    search_fields = ("name", "slug", "description")
    readonly_fields = ("created_at", "updated_at", "part_count_display")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PartConfigurationInline]

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "description", "is_expression")
        }),
        ("Statistics", {
            "fields": ("part_count_display",),
            "classes": ("collapse",)
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def type_badge(self, obj: PosePreset) -> str:
        """Display pose type with badge styling."""
        badge_type = "Expression" if obj.is_expression else "Body Pose"
        color = "#FF6B6B" if obj.is_expression else "#4ECDC4"
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px;">{}</span>',
            color,
            badge_type
        )
    type_badge.short_description = "Type"

    def part_count(self, obj: PosePreset) -> int:
        """Return number of parts in this pose."""
        return obj.part_configurations.count()
    part_count.short_description = "Parts"

    def part_count_display(self, obj: PosePreset) -> int:
        """Display part count in readonly field."""
        return obj.part_configurations.count()
    part_count_display.short_description = "Number of Parts"


@admin.register(PartConfiguration)
class PartConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for PartConfiguration model."""
    list_display = (
        "pose_preset",
        "puppet_part",
        "position_display",
        "rotation",
        "z_index"
    )
    list_filter = ("pose_preset", "z_index")
    search_fields = ("pose_preset__name", "puppet_part__name")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("References", {
            "fields": ("pose_preset", "puppet_part")
        }),
        ("Positioning", {
            "fields": ("position_x", "position_y", "rotation", "scale")
        }),
        ("Layering", {
            "fields": ("z_index",)
        }),
        ("Metadata", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def position_display(self, obj: PartConfiguration) -> str:
        """Display position in readable format."""
        return f"({obj.position_x:.1f}, {obj.position_y:.1f})"
    position_display.short_description = "Position (X, Y)"

