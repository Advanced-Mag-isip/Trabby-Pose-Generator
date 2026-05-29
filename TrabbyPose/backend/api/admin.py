
from django.contrib import admin
from .models import Poses, Export, PoseSelection, User
# Register your models here.


admin.site.register(Poses)
admin.site.register(Export)
admin.site.register(PoseSelection)
admin.site.register(User)