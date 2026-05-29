from django.db import migrations
from django.utils import timezone
import random


def create_dummy_data(apps, schema_editor):

    User = apps.get_model("api", "User")
    Poses = apps.get_model("api", "Poses")
    PoseSelection = apps.get_model("api", "PoseSelection")
    Export = apps.get_model("api", "Export")

    # Create seed user (always)
    user = User.objects.create(
        first_name="Seed",
        last_name="User",
        user_name="seed_user",
        password="123",
        email_address="seed@test.com",
        is_permitted=1,
        created_at=timezone.now(),
        updated_at=timezone.now()
    )

    pose_names = [
        "Trabby_Happy",
        "Trabby_Sad",
        "Trabby_Angry",
        "Trabby_Excited",
        "Trabby_Sleepy",
        "Trabby_Dancing",
        "Trabby_Running",
        "Trabby_Waving",
        "Trabby_Jumping",
        "Trabby_Crying"
    ]

    for i in range(10):

        pose = Poses.objects.create(
            poses_fid=user,
            name_of_poses_generated=pose_names[i],
            configuration={
                "pose_id": i + 1,
                "pose_name": pose_names[i],
                "pose": {
                    "head": {
                        "asset": "default_head",
                        "x": random.randint(90, 110),
                        "y": random.randint(40, 60),
                    },
                    "limbs": {},
                    "torso": {},
                    "accessories": {}
                }
            },
            created_at=timezone.now()
        )

        PoseSelection.objects.create(
            pose_selection_fid=pose,
            selected_at=timezone.now()
        )

        Export.objects.create(
            export_fid=pose,
            created_at=timezone.now()
        )


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_remove_poses_is_predefined_poses_configuration"),
    ]

    operations = [
        migrations.RunPython(create_dummy_data, migrations.RunPython.noop),
    ]