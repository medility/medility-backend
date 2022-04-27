from urllib import request
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.response import Response
from .models import Society, DeviceType, CommunityActivityInfo, CommunityUserInfo, CommunityGroup, CommunityGroupInfo
from .serializers import SocietySerializer, DeviceTypeSerializer, ActivityByPeriodSerializer, LeaderBoardSerializer, CommunityProfileSerializer, CommunityGroupSerializer, CommunitySocietyUserListSerializer, CommunityMyGroupListSerializer, CommunityGroupMemListListSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import permissions
from knox.auth import TokenAuthentication
from django.db.models import Sum
from rest_framework.views import APIView


# from medilityapp.comunity import serializers
# Create your views here.

def getRank(info_list, community_id):
        rank = 0
        isExist = False
        for rankInfo in info_list:
            if rankInfo['community_user_id'] == community_id:
                rank += 1
                isExist = True
                break
            else:
                rank += 1
                isExist = False
        if isExist:
            return rank
        return 0


class SocietyList(ListAPIView):
    serializer_class = SocietySerializer

    def get_queryset(self):
        society_code = self.request.query_params.get('societycode', None)
        society_name = self.request.query_params.get('name', None)
        if society_code is not None:
            return Society.objects.filter(society_code__iexact=society_code)
        elif society_name is not None:
            return Society.objects.filter(name__icontains=society_name)
        return Society.objects.all()


class DeviceList(ListAPIView):
    serializer_class = DeviceTypeSerializer
    queryset = DeviceType.objects.all()


class ActivityStepByPeriodView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ActivityByPeriodSerializer

    def get_queryset(self):
        byDate = self.request.query_params.get('date', None)
        byMonth = self.request.query_params.get('month', None)
        byYear = self.request.query_params.get('year', None)
        if byDate is not None:
            return CommunityActivityInfo.objects.filter(activity_date=byDate, community_user__user=self.request.user)
        elif byMonth is not None:
            return CommunityActivityInfo.objects.filter(activity_date__month=byMonth, community_user__user=self.request.user)
        elif byYear is not None:
            return CommunityActivityInfo.objects.filter(activity_date__year=byYear, community_user__user=self.request.user)
        return CommunityActivityInfo.objects.all()


class ActivityStepByPeriodCreate(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ActivityByPeriodSerializer

    def createStepsRecord(self, activityInfo):
        activitySerializer = ActivityByPeriodSerializer(data=activityInfo)
        if(activitySerializer.is_valid()):
            activitySerializer.save()
            return {'msg': 'Activity created successfully'}
        return activitySerializer.errors

    def create(self, request, *args, **kwargs):
        activityInfo = request.data
        userInfo = CommunityUserInfo.objects.get(user=self.request.user).id
        activityInfo['community_user'] = userInfo
        try:
            oldActivityInfo = CommunityActivityInfo.objects.get(community_user=userInfo, activity_date=activityInfo['activity_date'])
            if(oldActivityInfo):
                oldActivityInfo.delete()
            return Response(self.createStepsRecord(activityInfo))
        except:
            return Response(self.createStepsRecord(activityInfo))
        

class ActivityStepByWeekView(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ActivityByPeriodSerializer

    def get_queryset(self):
        fromDate = self.request.query_params.get('from', None)
        toDate = self.request.query_params.get('to', None)
        return CommunityActivityInfo.objects.filter(activity_date__range=(fromDate, toDate), community_user__user=self.request.user)


class LeaderBoardView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    def getFormattedResponse(self, queryInfo):
        result = []
        for userInfo in queryInfo:
            user = CommunityUserInfo.objects.get(id=userInfo['community_user_id'])
            res = {'name': user.user.name, 'community_id': userInfo['community_user_id'], 'steps': userInfo['completed_steps']}
            result.append(res)
        return result

    def get(self, request):
        type = self.request.query_params.get('type', None)
        community_user_info = CommunityUserInfo.objects.get(user=self.request.user)
        print(type)
        print(community_user_info.pincode)
        if type and type == '0':
            print("inside")
            pincodeInfo = CommunityActivityInfo.objects.filter(community_user__pincode=community_user_info.pincode).values('community_user_id').order_by().annotate(completed_steps=Sum('completed_steps')).order_by('-completed_steps')
            pincodeRank = getRank(pincodeInfo, community_user_info.id)
            userRankInfo = self.getFormattedResponse(pincodeInfo)
            return Response({'data': userRankInfo, 'rank': pincodeRank})
        elif type and type == '1':
            cityInfo = CommunityActivityInfo.objects.filter(community_user__city=community_user_info.city).values('community_user_id').order_by().annotate(completed_steps=Sum('completed_steps')).order_by('-completed_steps')
            cityRank = getRank(cityInfo, community_user_info.id)
            userRankInfo = self.getFormattedResponse(cityInfo)
            return Response({'data': userRankInfo, 'rank': cityRank})
        elif type and type == '2':
            societyInfo = CommunityActivityInfo.objects.filter(community_user__society=community_user_info.society).values('community_user_id').order_by().annotate(completed_steps=Sum('completed_steps')).order_by('-completed_steps')
            societyRank = getRank(societyInfo, community_user_info.id)
            userRankInfo = self.getFormattedResponse(societyInfo)
            return Response({'data': userRankInfo, 'rank': societyRank})
        elif type and type == '3':
            countryInfo = CommunityActivityInfo.objects.filter(community_user__country=community_user_info.country).values('community_user_id').order_by().annotate(completed_steps=Sum('completed_steps')).order_by('-completed_steps')
            countryRank = getRank(countryInfo, community_user_info.id)
            userRankInfo = self.getFormattedResponse(countryInfo)
            return Response({'data': userRankInfo, 'rank': countryRank})
        return CommunityActivityInfo.objects.values('community_user_id').order_by().annotate(completed_steps=Sum('completed_steps'))
         

class CommunityProfileView(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CommunityProfileSerializer

    def create(self, request, *args, **kwargs):
        profileInfo = request.data
        profileInfo['user'] = request.user.id
        serializer = self.get_serializer(data=profileInfo)
        if(serializer.is_valid()):
            serializer.save()
            return Response({'msg': 'Profile created successfully', 'status': 'success'})
        return Response(serializer.errors)


class CommunityCheckUser(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CommunityProfileSerializer

    def get(self, request):
        try:
            user = CommunityUserInfo.objects.get(user=self.request.user)
            if user:
                user_serializer = CommunityProfileSerializer(user)
                if user_serializer.is_valid:
                    return Response({'status': 'success', 'msg': 'User already configured', 'community_info': user_serializer.data})
        except CommunityUserInfo.DoesNotExist:
            return Response({'status': 'fail', 'msg': 'User not configured'})


class CommunityRank(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    

    def get(self, request):
        rankList = []
        community_user_info = CommunityUserInfo.objects.get(user=self.request.user)

        pincode_list = CommunityActivityInfo.objects.filter(community_user__pincode=community_user_info.pincode).values('community_user_id').order_by().annotate(completed_steps=Sum('completed_steps')).order_by('-completed_steps')
        pincodeRank = getRank(pincode_list, community_user_info.id)
        rankList.append({'type': 'pincode', 'val': community_user_info.pincode, 'rank': pincodeRank})

        city_list = CommunityActivityInfo.objects.filter(community_user__city=community_user_info.city).values('community_user_id').order_by().annotate(completed_steps=Sum('completed_steps')).order_by('-completed_steps')
        cityRank = getRank(city_list, community_user_info.id)
        rankList.append({'type': 'city', 'val': community_user_info.city, 'rank': cityRank})

        society_list = CommunityActivityInfo.objects.filter(community_user__society=community_user_info.society).values('community_user_id').order_by().annotate(completed_steps=Sum('completed_steps')).order_by('-completed_steps')
        societyRank = getRank(society_list, community_user_info.id)
        rankList.append({'type': 'society', 'val': community_user_info.society.name, 'rank': societyRank})

        country_list = CommunityActivityInfo.objects.filter(community_user__country=community_user_info.country).values('community_user_id').order_by().annotate(completed_steps=Sum('completed_steps')).order_by('-completed_steps')
        countryRank = getRank(country_list, community_user_info.id)
        rankList.append({'type': 'country', 'val': community_user_info.country, 'rank': countryRank})

        return Response(rankList)


class CommunityGroupList(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CommunityGroupSerializer
    queryset = CommunityGroup.objects.all()


class CommunitySocietyUserList(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CommunitySocietyUserListSerializer
    
    def get_queryset(self):
        user = CommunityUserInfo.objects.get(user=self.request.user)
        society_info = Society.objects.get(society_code = user.society.society_code)
        societyUsers = CommunityUserInfo.objects.filter(society=society_info)
        query_res = []
        for mem in societyUsers:
            if mem.id != user.id:
                query_res.append(mem)
        return query_res 


class CommunityGroupCreate(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        groupName = self.request.data.get('group_name', None)
        memberList = self.request.data.get('mem_list', None)
        if groupName and memberList:
            group = CommunityGroup(name=groupName)
            group.save()
            user = CommunityUserInfo.objects.get(user=self.request.user)
            group_member = CommunityGroupInfo(communityUser=user, communityGroupInfo=group, status=True, isAdmin=True)
            group_member.save()
            for member in memberList:
                user = CommunityUserInfo.objects.get(id=member)
                group_member = CommunityGroupInfo(communityUser=user, communityGroupInfo=group, status=False, isAdmin=False)
                group_member.save()
            return Response({'msg': 'created'})
        return Response({'msg': 'unable to created'})


class CommunityMyGroupList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        res = []
        user = CommunityUserInfo.objects.get(user=self.request.user)
        member = CommunityGroupInfo.objects.filter(communityUser=user, isAdmin=True)
        memSerialize = CommunityMyGroupListSerializer(member, many=True)
        for grpInfo in memSerialize.data:
            group = CommunityGroup.objects.get(id=grpInfo['communityGroupInfo']['id'])
            memCountOfEachInfo = CommunityGroupInfo.objects.filter(communityGroupInfo=group)
            memCount = {'group_info': grpInfo['communityGroupInfo'], 'members': memCountOfEachInfo.count()}
            res.append(memCount)
        return Response(res)
        

class CommunityMemOfGroup(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CommunityGroupMemListListSerializer


    def get_queryset(self):
        grp_id = self.request.GET.get('groupid', None)
        statusInfo = self.request.GET.get('status', None)
        print(grp_id)
        group = CommunityGroup.objects.get(id=grp_id)
        grp_info = CommunityGroupInfo.objects.filter(communityGroupInfo=group, isAdmin=False, status=statusInfo)
        return grp_info

    