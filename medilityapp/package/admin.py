from django.contrib import admin
from .models import Package, PackageDetail
# Register your models here.


admin.site.register(Package),
admin.site.register(PackageDetail)

