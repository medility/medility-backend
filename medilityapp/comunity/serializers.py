from django.db.models import fields
from .models import Society, DeviceType, CommunityActivityInfo, CommunityUserInfo, CommunityGroup, CommunityGroupInfo
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class SocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = '__all__'


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceType
        fields = '__all__'


class ActivityByPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityActivityInfo
        fields = '__all__'


class LeaderBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityActivityInfo
        fields = ['community_user_id', 'completed_steps']


class CommunityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityUserInfo
        fields = '__all__'


class CommunityGroupSerializer(serializers.ModelSerializer):
    communityUser = CommunityProfileSerializer(many=True)

    class Meta:
        model = CommunityGroup
        fields = ['id', 'name', 'communityUser']


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ('name','id')


class CommunitySocietyUserListSerializer(serializers.ModelSerializer):
    society = SocietySerializer()
    user = UserSerializer()

    class Meta:
        model = CommunityUserInfo
        fields = ['id', 'user', 'society',]


class CommunityGroupUserListSerializer(serializers.ModelSerializer):
    # society = SocietySerializer()
    user = UserSerializer()

    class Meta:
        model = CommunityUserInfo
        fields = ['user',]


class CommunityGroupDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunityGroup
        fields = '__all__'


class CommunityMyGroupListSerializer(serializers.ModelSerializer):
    communityGroupInfo = CommunityGroupDataSerializer()
    # communityUser = CommunitySocietyUserListSerializer()

    class Meta:
        model = CommunityGroupInfo
        fields = ['communityGroupInfo',]


class CommunityGroupMemListListSerializer(serializers.ModelSerializer):
    # communityGroupInfo = CommunityGroupDataSerializer()
    communityUser = CommunityGroupUserListSerializer()

    class Meta:
        model = CommunityGroupInfo
        fields = ['communityUser',]