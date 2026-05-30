"""
Django management command to seed the database with initial puppet assets,
preset poses, expressions, and their configurations.

Usage:
    python manage.py seed_assets
    python manage.py seed_assets --clear  (to clear and reseed)
"""

from typing import Dict, List, Tuple
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import PuppetPart, PosePreset, PartConfiguration


class Command(BaseCommand):
    """
    Management command to seed initial database with puppet assets
    and preset configurations.
    """

    help = "Seed the database with initial puppet parts, poses, and expressions"

    def add_arguments(self, parser):
        """Define command-line arguments."""
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """Execute the seeding operation."""
        if options["clear"]:
            self._clear_existing_data()

        try:
            self._seed_puppet_parts()
            self._seed_body_poses()
            self._seed_expressions()
            self.stdout.write(
                self.style.SUCCESS("✓ Database seeded successfully!")
            )
        except Exception as e:
            raise CommandError(f"Seeding failed: {str(e)}")

    def _clear_existing_data(self):
        """Clear all puppet-related data from database."""
        self.stdout.write("Clearing existing data...")
        PartConfiguration.objects.all().delete()
        PosePreset.objects.all().delete()
        PuppetPart.objects.all().delete()
        self.stdout.write(self.style.WARNING("✓ Existing data cleared"))

    def _seed_puppet_parts(self):
        """Create initial puppet parts/assets."""
        self.stdout.write("Seeding puppet parts...")

        parts_data: List[Dict] = [
            # ===== HEAD PARTS =====
            # Face
            {
                "name": "Face Round",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.FACE,
                "asset_url": "/assets/trabby/sprites/head_face_round.svg",
                "description": "A friendly round face for Trabby"
            },
            {
                "name": "Face Square",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.FACE,
                "asset_url": "/assets/trabby/sprites/head_face_square.svg",
                "description": "A bold square-shaped face"
            },
            # Eyes
            {
                "name": "Eyes Neutral",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.EYES,
                "asset_url": "/assets/trabby/sprites/eyes_neutral.svg",
                "description": "Neutral expression eyes"
            },
            {
                "name": "Eyes Happy",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.EYES,
                "asset_url": "/assets/trabby/sprites/eyes_happy.svg",
                "description": "Happy expression eyes (closed, smiling)"
            },
            {
                "name": "Eyes Surprised",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.EYES,
                "asset_url": "/assets/trabby/sprites/eyes_surprised.svg",
                "description": "Surprised expression eyes (wide open)"
            },
            {
                "name": "Eyes Confident",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.EYES,
                "asset_url": "/assets/trabby/sprites/eyes_confident.svg",
                "description": "Confident expression eyes (determined)"
            },
            # Mouth
            {
                "name": "Mouth Neutral",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.MOUTH,
                "asset_url": "/assets/trabby/sprites/mouth_neutral.svg",
                "description": "Neutral mouth"
            },
            {
                "name": "Mouth Smile",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.MOUTH,
                "asset_url": "/assets/trabby/sprites/mouth_smile.svg",
                "description": "Happy smile"
            },
            {
                "name": "Mouth Open",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.MOUTH,
                "asset_url": "/assets/trabby/sprites/mouth_open.svg",
                "description": "Surprised open mouth"
            },
            # Ears
            {
                "name": "Ears Standard",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.EARS,
                "asset_url": "/assets/trabby/sprites/ears_standard.svg",
                "description": "Standard ears"
            },
            {
                "name": "Ears Pointed",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.EARS,
                "asset_url": "/assets/trabby/sprites/ears_pointed.svg",
                "description": "Pointed elf-like ears"
            },
            # Hair
            {
                "name": "Hair Short",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.HAIR,
                "asset_url": "/assets/trabby/sprites/hair_short.svg",
                "description": "Short hair style"
            },
            {
                "name": "Hair Long",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.HAIR,
                "asset_url": "/assets/trabby/sprites/hair_long.svg",
                "description": "Long hair style"
            },
            # Eyebrows
            {
                "name": "Eyebrows Normal",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.EYEBROWS,
                "asset_url": "/assets/trabby/sprites/eyebrows_normal.svg",
                "description": "Normal eyebrows"
            },
            {
                "name": "Eyebrows Angry",
                "category": PuppetPart.Category.HEAD,
                "part_type": PuppetPart.PartType.EYEBROWS,
                "asset_url": "/assets/trabby/sprites/eyebrows_angry.svg",
                "description": "Angry eyebrows"
            },

            # ===== LIMB PARTS =====
            # Left Upper Arm
            {
                "name": "Left Upper Arm Up",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.LEFT_UPPER_ARM,
                "asset_url": "/assets/trabby/sprites/left_upper_arm_up.svg",
                "description": "Left upper arm raised upward"
            },
            {
                "name": "Left Upper Arm Down",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.LEFT_UPPER_ARM,
                "asset_url": "/assets/trabby/sprites/left_upper_arm_down.svg",
                "description": "Left upper arm at rest"
            },
            # Right Upper Arm
            {
                "name": "Right Upper Arm Up",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.RIGHT_UPPER_ARM,
                "asset_url": "/assets/trabby/sprites/right_upper_arm_up.svg",
                "description": "Right upper arm raised upward"
            },
            {
                "name": "Right Upper Arm Down",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.RIGHT_UPPER_ARM,
                "asset_url": "/assets/trabby/sprites/right_upper_arm_down.svg",
                "description": "Right upper arm at rest"
            },
            # Left Forearm & Hand
            {
                "name": "Left Forearm & Hand Neutral",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.LEFT_FOREARM_HAND,
                "asset_url": "/assets/trabby/sprites/left_forearm_hand_neutral.svg",
                "description": "Left forearm and hand in neutral position"
            },
            {
                "name": "Left Forearm & Hand Pointing",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.LEFT_FOREARM_HAND,
                "asset_url": "/assets/trabby/sprites/left_forearm_hand_pointing.svg",
                "description": "Left forearm and hand pointing"
            },
            # Right Forearm & Hand
            {
                "name": "Right Forearm & Hand Neutral",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.RIGHT_FOREARM_HAND,
                "asset_url": "/assets/trabby/sprites/right_forearm_hand_neutral.svg",
                "description": "Right forearm and hand in neutral position"
            },
            {
                "name": "Right Forearm & Hand Thumbs Up",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.RIGHT_FOREARM_HAND,
                "asset_url": "/assets/trabby/sprites/right_forearm_hand_thumbs_up.svg",
                "description": "Right forearm and hand giving thumbs up"
            },
            # Left Thigh
            {
                "name": "Left Thigh Neutral",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.LEFT_THIGH,
                "asset_url": "/assets/trabby/sprites/left_thigh_neutral.svg",
                "description": "Left thigh in neutral position"
            },
            {
                "name": "Left Thigh Bent",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.LEFT_THIGH,
                "asset_url": "/assets/trabby/sprites/left_thigh_bent.svg",
                "description": "Left thigh bent at knee"
            },
            # Right Thigh
            {
                "name": "Right Thigh Neutral",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.RIGHT_THIGH,
                "asset_url": "/assets/trabby/sprites/right_thigh_neutral.svg",
                "description": "Right thigh in neutral position"
            },
            {
                "name": "Right Thigh Bent",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.RIGHT_THIGH,
                "asset_url": "/assets/trabby/sprites/right_thigh_bent.svg",
                "description": "Right thigh bent at knee"
            },
            # Left Lower Leg & Foot
            {
                "name": "Left Lower Leg & Foot Neutral",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.LEFT_LOWER_LEG_FOOT,
                "asset_url": "/assets/trabby/sprites/left_lower_leg_foot_neutral.svg",
                "description": "Left lower leg and foot in neutral position"
            },
            {
                "name": "Left Lower Leg & Foot Extended",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.LEFT_LOWER_LEG_FOOT,
                "asset_url": "/assets/trabby/sprites/left_lower_leg_foot_extended.svg",
                "description": "Left lower leg and foot extended"
            },
            # Right Lower Leg & Foot
            {
                "name": "Right Lower Leg & Foot Neutral",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.RIGHT_LOWER_LEG_FOOT,
                "asset_url": "/assets/trabby/sprites/right_lower_leg_foot_neutral.svg",
                "description": "Right lower leg and foot in neutral position"
            },
            {
                "name": "Right Lower Leg & Foot Extended",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.RIGHT_LOWER_LEG_FOOT,
                "asset_url": "/assets/trabby/sprites/right_lower_leg_foot_extended.svg",
                "description": "Right lower leg and foot extended"
            },
            # Tail
            {
                "name": "Tail Down",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.TAIL,
                "asset_url": "/assets/trabby/sprites/tail_down.svg",
                "description": "Tail hanging down"
            },
            {
                "name": "Tail Up",
                "category": PuppetPart.Category.LIMBS,
                "part_type": PuppetPart.PartType.TAIL,
                "asset_url": "/assets/trabby/sprites/tail_up.svg",
                "description": "Tail raised up"
            },

            # ===== TORSO PARTS =====
            {
                "name": "Standard Torso",
                "category": PuppetPart.Category.TORSO,
                "part_type": PuppetPart.PartType.TORSO_BODY,
                "asset_url": "/assets/trabby/sprites/torso_standard.svg",
                "description": "Standard rectangular torso"
            },
            {
                "name": "Athletic Torso",
                "category": PuppetPart.Category.TORSO,
                "part_type": PuppetPart.PartType.TORSO_BODY,
                "asset_url": "/assets/trabby/sprites/torso_athletic.svg",
                "description": "More muscular torso variant"
            },

            # ===== ACCESSORY PARTS =====
            # Wearables
            {
                "name": "Hat Top",
                "category": PuppetPart.Category.ACCESSORIES,
                "part_type": PuppetPart.PartType.WEARABLES,
                "asset_url": "/assets/trabby/sprites/hat_top.svg",
                "description": "Top hat accessory"
            },
            {
                "name": "Scarf",
                "category": PuppetPart.Category.ACCESSORIES,
                "part_type": PuppetPart.PartType.WEARABLES,
                "asset_url": "/assets/trabby/sprites/scarf.svg",
                "description": "Scarf accessory"
            },
            # Holdables
            {
                "name": "Staff",
                "category": PuppetPart.Category.ACCESSORIES,
                "part_type": PuppetPart.PartType.HOLDABLES,
                "asset_url": "/assets/trabby/sprites/staff.svg",
                "description": "Magic staff prop"
            },
            {
                "name": "Sword",
                "category": PuppetPart.Category.ACCESSORIES,
                "part_type": PuppetPart.PartType.HOLDABLES,
                "asset_url": "/assets/trabby/sprites/sword.svg",
                "description": "Sword prop"
            },
        ]

        for part_data in parts_data:
            part, created = PuppetPart.objects.get_or_create(
                name=part_data["name"],
                part_type=part_data["part_type"],
                defaults={
                    "category": part_data["category"],
                    "asset_url": part_data["asset_url"],
                    "description": part_data.get("description", "")
                }
            )
            if created:
                self.stdout.write(f"  ✓ Created: {part.name}")
            else:
                self.stdout.write(f"  • Exists: {part.name}")

    def _seed_body_poses(self):
        """Create preset body poses."""
        self.stdout.write("Seeding body poses...")

        # Fetch puppet parts (assume they exist from previous seed)
        parts = {
            part.name: part
            for part in PuppetPart.objects.all()
        }

        poses_data: List[Dict] = [
            {
                "name": "Neutral",
                "slug": "neutral",
                "description": "Character standing in neutral pose with arms at sides",
                "is_expression": False,
                "parts": [
                    ("Round Head", {"x": 200, "y": 100, "rotation": 0, "z": 5}),
                    ("Standard Torso", {"x": 200, "y": 180, "rotation": 0, "z": 4}),
                    ("Left Arm Down", {"x": 160, "y": 200, "rotation": 0, "z": 3}),
                    ("Right Arm Down", {"x": 240, "y": 200, "rotation": 0, "z": 3}),
                    ("Left Leg", {"x": 190, "y": 280, "rotation": 0, "z": 2}),
                    ("Right Leg", {"x": 210, "y": 280, "rotation": 0, "z": 2}),
                ]
            },
            {
                "name": "Thumbs Up",
                "slug": "thumbs-up",
                "description": "Character giving enthusiastic thumbs up with right hand",
                "is_expression": False,
                "parts": [
                    ("Round Head", {"x": 200, "y": 100, "rotation": 0, "z": 5}),
                    ("Standard Torso", {"x": 200, "y": 180, "rotation": 0, "z": 4}),
                    ("Left Arm Down", {"x": 160, "y": 200, "rotation": 0, "z": 3}),
                    ("Right Arm Up", {"x": 240, "y": 120, "rotation": 0, "z": 3}),
                    ("Thumbs Up Hand", {"x": 250, "y": 80, "rotation": 0, "z": 2}),
                    ("Left Leg", {"x": 190, "y": 280, "rotation": 0, "z": 1}),
                    ("Right Leg", {"x": 210, "y": 280, "rotation": 0, "z": 1}),
                ]
            },
            {
                "name": "Pointing",
                "slug": "pointing",
                "description": "Character pointing forward with right hand",
                "is_expression": False,
                "parts": [
                    ("Round Head", {"x": 200, "y": 100, "rotation": 0, "z": 5}),
                    ("Standard Torso", {"x": 200, "y": 180, "rotation": 0, "z": 4}),
                    ("Left Arm Down", {"x": 160, "y": 200, "rotation": 0, "z": 3}),
                    ("Right Arm Up", {"x": 260, "y": 160, "rotation": 45, "z": 3}),
                    ("Pointing Hand", {"x": 290, "y": 130, "rotation": 45, "z": 2}),
                    ("Left Leg", {"x": 190, "y": 280, "rotation": 0, "z": 1}),
                    ("Right Leg", {"x": 210, "y": 280, "rotation": 0, "z": 1}),
                ]
            },
        ]

        for pose_data in poses_data:
            pose, created = PosePreset.objects.get_or_create(
                slug=pose_data["slug"],
                defaults={
                    "name": pose_data["name"],
                    "description": pose_data["description"],
                    "is_expression": pose_data["is_expression"],
                }
            )

            if created:
                self.stdout.write(f"  ✓ Created pose: {pose.name}")
            else:
                self.stdout.write(f"  • Exists: {pose.name}")

            # Create part configurations
            for part_name, config_data in pose_data["parts"]:
                if part_name in parts:
                    config, created = PartConfiguration.objects.get_or_create(
                        pose_preset=pose,
                        puppet_part=parts[part_name],
                        defaults={
                            "position_x": config_data["x"],
                            "position_y": config_data["y"],
                            "rotation": config_data["rotation"],
                            "z_index": config_data["z"],
                            "scale": 1.0,
                        }
                    )
                    if created:
                        self.stdout.write(
                            f"    ✓ Added part: {part_name}"
                        )

    def _seed_expressions(self):
        """Create preset facial expressions."""
        self.stdout.write("Seeding facial expressions...")

        parts = {
            part.name: part
            for part in PuppetPart.objects.all()
        }

        expressions_data: List[Dict] = [
            {
                "name": "Happy",
                "slug": "happy",
                "description": "Cheerful facial expression with smile",
                "is_expression": True,
                "parts": [
                    ("Eyes Happy", {"x": 185, "y": 110, "rotation": 0, "z": 10}),
                    ("Mouth Smile", {"x": 200, "y": 140, "rotation": 0, "z": 9}),
                ]
            },
            {
                "name": "Surprised",
                "slug": "surprised",
                "description": "Shocked or amazed facial expression",
                "is_expression": True,
                "parts": [
                    ("Eyes Surprised", {"x": 185, "y": 110, "rotation": 0, "z": 10}),
                    ("Mouth Open", {"x": 200, "y": 140, "rotation": 0, "z": 9}),
                ]
            },
            {
                "name": "Confident",
                "slug": "confident",
                "description": "Determined and confident facial expression",
                "is_expression": True,
                "parts": [
                    ("Eyes Confident", {"x": 185, "y": 110, "rotation": 0, "z": 10}),
                    ("Mouth Neutral", {"x": 200, "y": 140, "rotation": 0, "z": 9}),
                ]
            },
        ]

        for expr_data in expressions_data:
            expr, created = PosePreset.objects.get_or_create(
                slug=expr_data["slug"],
                defaults={
                    "name": expr_data["name"],
                    "description": expr_data["description"],
                    "is_expression": expr_data["is_expression"],
                }
            )

            if created:
                self.stdout.write(f"  ✓ Created expression: {expr.name}")
            else:
                self.stdout.write(f"  • Exists: {expr.name}")

            # Create part configurations
            for part_name, config_data in expr_data["parts"]:
                if part_name in parts:
                    config, created = PartConfiguration.objects.get_or_create(
                        pose_preset=expr,
                        puppet_part=parts[part_name],
                        defaults={
                            "position_x": config_data["x"],
                            "position_y": config_data["y"],
                            "rotation": config_data["rotation"],
                            "z_index": config_data["z"],
                            "scale": 1.0,
                        }
                    )
                    if created:
                        self.stdout.write(
                            f"    ✓ Added part: {part_name}"
                        )
