from django.db import models

#User
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    user_name = models.CharField(max_length=225)
    password = models.CharField(max_length=225)
    email_address = models.CharField(max_length=225)
    is_permitted = models.IntegerField()
    created_at = models.DateTimeField(null=True, blank=False)
    updated_at = models.DateTimeField(null=True, blank=False)

#Poses Model
class Poses(models.Model):
    poses_id = models.AutoField(primary_key=True)

    poses_fid = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name_of_poses_generated = models.CharField(max_length=225)
    # is_predefined = models.BooleanField(default=False)
    configuration = models.JSONField(default=list)
    created_at = models.DateTimeField(null=True, blank=True)

class PoseSelection(models.Model):
    pose_selection_id = models.AutoField(primary_key=True)

    pose_selection_fid = models.ForeignKey(
        Poses,
        on_delete=models.CASCADE
    )
    selected_at = models.DateTimeField(null=True, blank=True)
#Export Model
class Export(models.Model):
    export_id = models.AutoField(primary_key=True)
    export_fid = models.ForeignKey(
        Poses,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(null=True, blank=True)

class PuppetPart(models.Model):
    """
    Represents a single puppet asset organized in a hierarchical structure:
    Category (Head, Limbs, Torso, Accessories) 
      → Subcategory (Face, Eyes, Mouth, etc.)
        → Option (specific asset like 'head-1', 'Round Eyes', etc.)
    """

    class Category(models.TextChoices):
        """Main categories matching the Customization UI structure."""
        HEAD = "Head", "Head"
        LIMBS = "Limbs", "Limbs"
        TORSO = "Torso", "Torso"
        ACCESSORIES = "Accessories", "Accessories"

    id = models.AutoField(primary_key=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        help_text="Main category (Head, Limbs, Torso, Accessories)"
    )
    subcategory = models.CharField(
        max_length=100,
        help_text="Subcategory within the category (e.g., 'Face', 'Eyes', 'Left Upper Arm')"
    )
    name = models.CharField(
        max_length=100,
        help_text="Display name for this specific option (e.g., 'Round Eyes', 'head-1')"
    )
    asset_url = models.CharField(
        max_length=500,
        help_text="URL or file path to the asset image/SVG"
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Optional description for documentation"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order within subcategory"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "subcategory", "order", "name"]
        verbose_name = "Puppet Part"
        verbose_name_plural = "Puppet Parts"
        unique_together = [["category", "subcategory", "name"]]
        indexes = [
            models.Index(fields=["category", "subcategory"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.subcategory} / {self.category})"


class PosePreset(models.Model):
    """Represents a pre-configured preset pose/expression layout."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100,
        help_text="Display name for the pose (e.g., 'Thumbs Up', 'Happy Expression')"
    )
    slug = models.SlugField(
        unique=True,
        max_length=100,
        help_text="URL-safe unique identifier (e.g., 'thumbs-up', 'happy')"
    )
    description = models.TextField(
        blank=True,
        default="",
        help_text="Detailed description of the pose"
    )
    is_expression = models.BooleanField(
        default=False,
        help_text="True if this is a facial expression; False if body pose"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pose Preset"
        verbose_name_plural = "Pose Presets"

    def __str__(self) -> str:
        return f"{self.name} ({'Expression' if self.is_expression else 'Pose'})"


class PartConfiguration(models.Model):
    """
    Junction table mapping a PosePreset to a PuppetPart with positioning,
    rotation, and layering information.
    """

    id = models.AutoField(primary_key=True)
    pose_preset = models.ForeignKey(
        PosePreset,
        on_delete=models.CASCADE,
        related_name="part_configurations",
        help_text="Reference to the pose preset"
    )
    puppet_part = models.ForeignKey(
        PuppetPart,
        on_delete=models.CASCADE,
        related_name="configurations",
        help_text="Reference to the puppet part asset"
    )
    position_x = models.FloatField(
        default=0.0,
        help_text="X coordinate position (pixels or normalized units)"
    )
    position_y = models.FloatField(
        default=0.0,
        help_text="Y coordinate position (pixels or normalized units)"
    )
    rotation = models.FloatField(
        default=0.0,
        help_text="Rotation angle in degrees (0-360)"
    )
    z_index = models.IntegerField(
        default=0,
        help_text="Layer ordering (higher values appear on top)"
    )
    scale = models.FloatField(
        default=1.0,
        help_text="Scale multiplier for the part (e.g., 1.0 = 100%)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["z_index", "puppet_part"]
        verbose_name = "Part Configuration"
        verbose_name_plural = "Part Configurations"
        unique_together = [["pose_preset", "puppet_part"]]

    def __str__(self) -> str:
        return f"{self.pose_preset.name} - {self.puppet_part.name} (Z: {self.z_index})"