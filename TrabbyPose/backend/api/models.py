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
    is_predefined = models.BooleanField(default=False)
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