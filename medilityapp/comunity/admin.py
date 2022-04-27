from django.contrib import admin
from .models import Society, DeviceType, CommunityUserInfo, CommunityActivityInfo, CommunityGroup, CommunityGroupInfo
# Register your models here.

admin.site.register(Society),
admin.site.register(DeviceType),
admin.site.register(CommunityUserInfo),
admin.site.register(CommunityActivityInfo),
admin.site.register(CommunityGroup),
admin.site.register(CommunityGroupInfo),


