"""
Django management command to seed the database with initial puppet assets,
organized in the hierarchical structure matching the Customization UI.

Usage:
    python manage.py seed_assets
    python manage.py seed_assets --clear  (to clear and reseed)
"""

from typing import Dict, List
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import PuppetPart, PosePreset, PartConfiguration


class Command(BaseCommand):
    """
    Management command to seed initial database with puppet assets
    organized hierarchically: Category → Subcategory → Options
    """

    help = "Seed the database with initial puppet parts organized hierarchically"

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
        """
        Create initial puppet parts/assets organized hierarchically.
        
        Structure matches Customization.astro exactly.
        """
        self.stdout.write("Seeding puppet parts hierarchically...")

        # Exact copy of the Customization.astro frontend TABS object model
        parts_hierarchy: Dict[str, Dict[str, List[Dict]]] = {
            "Head": {
                "Head Position": [
                    {"name": "head-1", "asset_url": "/assets/trabby/sprites/head-1.png"},
                    {"name": "head-2", "asset_url": "/assets/trabby/sprites/head-2.png"},
                    {"name": "Tilted Right", "asset_url": "/assets/trabby/sprites/head-tilted-right.png"},
                    {"name": "Looking Up", "asset_url": "/assets/trabby/sprites/head-looking-up.png"},
                    {"name": "Looking Down", "asset_url": "/assets/trabby/sprites/head-looking-down.png"},
                    {"name": "Bowed", "asset_url": "/assets/trabby/sprites/head-bowed.png"},
                ],
                "Face": [
                    {"name": "face-1", "asset_url": "/assets/trabby/sprites/face-1.png"},
                    {"name": "face-2", "asset_url": "/assets/trabby/sprites/face-2.png"},
                    {"name": "Star Eyes", "asset_url": "/assets/trabby/sprites/face-star-eyes.png"},
                    {"name": "Heart Eyes", "asset_url": "/assets/trabby/sprites/face-heart-eyes.png"},
                    {"name": "Dot Eyes", "asset_url": "/assets/trabby/sprites/face-dot-eyes.png"},
                    {"name": "Winking", "asset_url": "/assets/trabby/sprites/face-winking.png"},
                ],
                "Eyes": [
                    {"name": "Round Eyes", "asset_url": "/assets/trabby/sprites/eyes-round.png"},
                    {"name": "Sleepy Eyes", "asset_url": "/assets/trabby/sprites/eyes-sleepy.png"},
                    {"name": "Star Eyes", "asset_url": "/assets/trabby/sprites/eyes-star.png"},
                    {"name": "Heart Eyes", "asset_url": "/assets/trabby/sprites/eyes-heart.png"},
                    {"name": "Dot Eyes", "asset_url": "/assets/trabby/sprites/eyes-dot.png"},
                    {"name": "Winking", "asset_url": "/assets/trabby/sprites/eyes-winking.png"},
                ],
                "Mouth": [
                    {"name": "Smile", "asset_url": "/assets/trabby/sprites/mouth-smile.png"},
                    {"name": "Grin", "asset_url": "/assets/trabby/sprites/mouth-grin.png"},
                    {"name": "Pout", "asset_url": "/assets/trabby/sprites/mouth-pout.png"},
                    {"name": "Open Mouth", "asset_url": "/assets/trabby/sprites/mouth-open.png"},
                    {"name": "Smirk", "asset_url": "/assets/trabby/sprites/mouth-smirk.png"},
                    {"name": "Frown", "asset_url": "/assets/trabby/sprites/mouth-frown.png"},
                ],
                "Ears": [
                    {"name": "Round Ears", "asset_url": "/assets/trabby/sprites/ears-round.png"},
                    {"name": "Pointy Ears", "asset_url": "/assets/trabby/sprites/ears-pointy.png"},
                    {"name": "Floppy Ears", "asset_url": "/assets/trabby/sprites/ears-floppy.png"},
                    {"name": "No Ears", "asset_url": "/assets/trabby/sprites/ears-none.png"},
                    {"name": "Cat Ears", "asset_url": "/assets/trabby/sprites/ears-cat.png"},
                    {"name": "Bear Ears", "asset_url": "/assets/trabby/sprites/ears-bear.png"},
                ],
                "Hair": [
                    {"name": "No Hair", "asset_url": "/assets/trabby/sprites/hair-none.png"},
                    {"name": "Short Tuft", "asset_url": "/assets/trabby/sprites/hair-short-tuft.png"},
                    {"name": "Long Tuft", "asset_url": "/assets/trabby/sprites/hair-long-tuft.png"},
                    {"name": "Spiky", "asset_url": "/assets/trabby/sprites/hair-spiky.png"},
                    {"name": "Wavy", "asset_url": "/assets/trabby/sprites/hair-wavy.png"},
                    {"name": "Bun", "asset_url": "/assets/trabby/sprites/hair-bun.png"},
                ],
                "Eyebrows": [
                    {"name": "Normal", "asset_url": "/assets/trabby/sprites/eyebrows-normal.png"},
                    {"name": "Raised", "asset_url": "/assets/trabby/sprites/eyebrows-raised.png"},
                    {"name": "Furrowed", "asset_url": "/assets/trabby/sprites/eyebrows-furrowed.png"},
                    {"name": "Thin", "asset_url": "/assets/trabby/sprites/eyebrows-thin.png"},
                    {"name": "Bushy", "asset_url": "/assets/trabby/sprites/eyebrows-bushy.png"},
                    {"name": "Arched", "asset_url": "/assets/trabby/sprites/eyebrows-arched.png"},
                ],
            },
            "Limbs": {
                "Limbs": [
                    {"name": "limbs-1", "asset_url": "/assets/trabby/sprites/limbs-1.png"},
                    {"name": "limbs-2", "asset_url": "/assets/trabby/sprites/limbs-2.png"},
                ],
                "Left Upper Arm": [
                    {"name": "Default", "asset_url": "/assets/trabby/sprites/left-upper-arm-default.png"},
                    {"name": "Raised", "asset_url": "/assets/trabby/sprites/left-upper-arm-raised.png"},
                    {"name": "Lowered", "asset_url": "/assets/trabby/sprites/left-upper-arm-lowered.png"},
                    {"name": "Crossed", "asset_url": "/assets/trabby/sprites/left-upper-arm-crossed.png"},
                    {"name": "Flexed", "asset_url": "/assets/trabby/sprites/left-upper-arm-flexed.png"},
                ],
                "Right Upper Arm": [
                    {"name": "Default", "asset_url": "/assets/trabby/sprites/right-upper-arm-default.png"},
                    {"name": "Raised", "asset_url": "/assets/trabby/sprites/right-upper-arm-raised.png"},
                    {"name": "Lowered", "asset_url": "/assets/trabby/sprites/right-upper-arm-lowered.png"},
                    {"name": "Crossed", "asset_url": "/assets/trabby/sprites/right-upper-arm-crossed.png"},
                    {"name": "Flexed", "asset_url": "/assets/trabby/sprites/right-upper-arm-flexed.png"},
                ],
                "Left Forearm & Hand": [
                    {"name": "Open Hand", "asset_url": "/assets/trabby/sprites/left-forearm-open-hand.png"},
                    {"name": "Fist", "asset_url": "/assets/trabby/sprites/left-forearm-fist.png"},
                    {"name": "Peace Sign", "asset_url": "/assets/trabby/sprites/left-forearm-peace-sign.png"},
                    {"name": "Pointing", "asset_url": "/assets/trabby/sprites/left-forearm-pointing.png"},
                    {"name": "Wave", "asset_url": "/assets/trabby/sprites/left-forearm-wave.png"},
                ],
                "Right Forearm & Hand": [
                    {"name": "Open Hand", "asset_url": "/assets/trabby/sprites/right-forearm-open-hand.png"},
                    {"name": "Fist", "asset_url": "/assets/trabby/sprites/right-forearm-fist.png"},
                    {"name": "Peace Sign", "asset_url": "/assets/trabby/sprites/right-forearm-peace-sign.png"},
                    {"name": "Pointing", "asset_url": "/assets/trabby/sprites/right-forearm-pointing.png"},
                    {"name": "Wave", "asset_url": "/assets/trabby/sprites/right-forearm-wave.png"},
                ],
                "Left Thigh": [
                    {"name": "Default", "asset_url": "/assets/trabby/sprites/left-thigh-default.png"},
                    {"name": "Wide Stance", "asset_url": "/assets/trabby/sprites/left-thigh-wide-stance.png"},
                    {"name": "Narrow Stance", "asset_url": "/assets/trabby/sprites/left-thigh-narrow-stance.png"},
                    {"name": "Crossed", "asset_url": "/assets/trabby/sprites/left-thigh-crossed.png"},
                ],
                "Right Thigh": [
                    {"name": "Default", "asset_url": "/assets/trabby/sprites/right-thigh-default.png"},
                    {"name": "Wide Stance", "asset_url": "/assets/trabby/sprites/right-thigh-wide-stance.png"},
                    {"name": "Narrow Stance", "asset_url": "/assets/trabby/sprites/right-thigh-narrow-stance.png"},
                    {"name": "Crossed", "asset_url": "/assets/trabby/sprites/right-thigh-crossed.png"},
                ],
                "Left Lower Leg & Foot": [
                    {"name": "Default", "asset_url": "/assets/trabby/sprites/left-lower-leg-default.png"},
                    {"name": "Tip-toe", "asset_url": "/assets/trabby/sprites/left-lower-leg-tiptoe.png"},
                    {"name": "Flat Foot", "asset_url": "/assets/trabby/sprites/left-lower-leg-flat.png"},
                    {"name": "Raised", "asset_url": "/assets/trabby/sprites/left-lower-leg-raised.png"},
                ],
                "Right Lower Leg & Foot": [
                    {"name": "Default", "asset_url": "/assets/trabby/sprites/right-lower-leg-default.png"},
                    {"name": "Tip-toe", "asset_url": "/assets/trabby/sprites/right-lower-leg-tiptoe.png"},
                    {"name": "Flat Foot", "asset_url": "/assets/trabby/sprites/right-lower-leg-flat.png"},
                    {"name": "Raised", "asset_url": "/assets/trabby/sprites/right-lower-leg-raised.png"},
                ],
                "Tail": [
                    {"name": "No Tail", "asset_url": "/assets/trabby/sprites/tail-none.png"},
                    {"name": "Short Tail", "asset_url": "/assets/trabby/sprites/tail-short.png"},
                    {"name": "Long Tail", "asset_url": "/assets/trabby/sprites/tail-long.png"},
                    {"name": "Curly Tail", "asset_url": "/assets/trabby/sprites/tail-curly.png"},
                    {"name": "Wagging Tail", "asset_url": "/assets/trabby/sprites/tail-wagging.png"},
                ],
            },
            "Torso": {
                "Torso Shape": [
                    {"name": "torso-1", "asset_url": "/assets/trabby/sprites/torso-1.png"},
                    {"name": "torso-2", "asset_url": "/assets/trabby/sprites/torso-2.png"},
                    {"name": "Chubby", "asset_url": "/assets/trabby/sprites/torso-chubby.png"},
                    {"name": "Slim", "asset_url": "/assets/trabby/sprites/torso-slim.png"},
                    {"name": "Muscular", "asset_url": "/assets/trabby/sprites/torso-muscular.png"},
                    {"name": "Round", "asset_url": "/assets/trabby/sprites/torso-round.png"},
                    {"name": "Tiny", "asset_url": "/assets/trabby/sprites/torso-tiny.png"},
                ],
            },
            "Accessories": {
                "Wearables": [
                    {"name": "acc-1", "asset_url": "/assets/trabby/sprites/acc-1.png"},
                    {"name": "acc-2", "asset_url": "/assets/trabby/sprites/acc-2.png"},
                    {"name": "Scarf", "asset_url": "/assets/trabby/sprites/acc-scarf.png"},
                    {"name": "Bowtie", "asset_url": "/assets/trabby/sprites/acc-bowtie.png"},
                    {"name": "Necklace", "asset_url": "/assets/trabby/sprites/acc-necklace.png"},
                    {"name": "Cape", "asset_url": "/assets/trabby/sprites/acc-cape.png"},
                    {"name": "Backpack", "asset_url": "/assets/trabby/sprites/acc-backpack.png"},
                    {"name": "Hat", "asset_url": "/assets/trabby/sprites/acc-hat.png"},
                    {"name": "Glasses", "asset_url": "/assets/trabby/sprites/acc-glasses.png"},
                    {"name": "Apron", "asset_url": "/assets/trabby/sprites/acc-apron.png"},
                    {"name": "Hoodie", "asset_url": "/assets/trabby/sprites/acc-hoodie.png"},
                ],
                "Holdables": [
                    {"name": "None", "asset_url": ""},
                    {"name": "Sword", "asset_url": "/assets/trabby/sprites/acc-sword.png"},
                    {"name": "Staff", "asset_url": "/assets/trabby/sprites/acc-staff.png"},
                    {"name": "Flower", "asset_url": "/assets/trabby/sprites/acc-flower.png"},
                    {"name": "Lantern", "asset_url": "/assets/trabby/sprites/acc-lantern.png"},
                    {"name": "Book", "asset_url": "/assets/trabby/sprites/acc-book.png"},
                    {"name": "Umbrella", "asset_url": "/assets/trabby/sprites/acc-umbrella.png"},
                    {"name": "Balloon", "asset_url": "/assets/trabby/sprites/acc-balloon.png"},
                    {"name": "Basket", "asset_url": "/assets/trabby/sprites/acc-basket.png"},
                ],
            },
        }

        # Flatten and create all PuppetPart objects
        created_count = 0
        exists_count = 0
        for category, subcategories in parts_hierarchy.items():
            for subcategory, options in subcategories.items():
                for order, option in enumerate(options):
                    part, created = PuppetPart.objects.get_or_create(
                        category=category,
                        subcategory=subcategory,
                        name=option["name"],
                        defaults={
                            "asset_url": option["asset_url"],
                            "order": order,
                            "description": f"{option['name']} from {subcategory}",
                        }
                    )
                    if created:
                        created_count += 1
                        self.stdout.write(f"  ✓ Created: [{category} -> {subcategory}] {part.name}")
                    else:
                        exists_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"✓ Finished processing parts: {created_count} created, {exists_count} already existed.")
        )

    def _seed_body_poses(self):
        """Create preset body poses."""
        self.stdout.write("Seeding body poses...")

        parts = {part.name: part for part in PuppetPart.objects.all()}

        poses_data: List[Dict] = [
            {
                "name": "Neutral",
                "slug": "neutral",
                "description": "Character standing in neutral pose with arms at sides",
                "is_expression": False,
                "parts": [
                    ("head-1", {"x": 200, "y": 100, "rotation": 0, "z": 5}),
                    ("torso-1", {"x": 200, "y": 180, "rotation": 0, "z": 4}),
                    ("Default", {"x": 160, "y": 200, "rotation": 0, "z": 3}),
                    ("Open Hand", {"x": 160, "y": 240, "rotation": 0, "z": 3}),
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

            for part_name, config_data in pose_data["parts"]:
                if part_name in parts:
                    PartConfiguration.objects.get_or_create(
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

    def _seed_expressions(self):
        """Create preset facial expressions."""
        self.stdout.write("Seeding facial expressions...")

        parts = {part.name: part for part in PuppetPart.objects.all()}

        expressions_data: List[Dict] = [
            {
                "name": "Happy",
                "slug": "happy",
                "description": "Cheerful facial expression with smile",
                "is_expression": True,
                "parts": [
                    ("Smile", {"x": 200, "y": 140, "rotation": 0, "z": 9}),
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

            for part_name, config_data in expr_data["parts"]:
                if part_name in parts:
                    PartConfiguration.objects.get_or_create(
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