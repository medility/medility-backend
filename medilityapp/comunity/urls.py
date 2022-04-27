from django.urls import path, include
from comunity import views

app_name = 'comunity'

urlpatterns = [
        path('society/', views.SocietyList.as_view()),
        path('device/', views.DeviceList.as_view()),
        path('steps/', views.ActivityStepByPeriodView.as_view()),
        path('steps/week/', views.ActivityStepByWeekView.as_view()),
        path('leaderboard/', views.LeaderBoardView.as_view()),
        path('profile/', views.CommunityProfileView.as_view()),
        path('checkuser/', views.CommunityCheckUser.as_view()),
        path('rank/', views.CommunityRank.as_view()),
        path('activity/create/', views.ActivityStepByPeriodCreate.as_view()),
        path('group/', views.CommunityGroupList.as_view()),
        path('societyuser/', views.CommunitySocietyUserList.as_view()),
        path('group/create/', views.CommunityGroupCreate.as_view()),
        path('mygroup/', views.CommunityMyGroupList.as_view()),
        path('grpmemlist/', views.CommunityMemOfGroup.as_view()),
]

