from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    YouthOrganizationListView, YouthOrganizationDetailView,
    YouthOrganizationCreateView, YouthOrganizationUpdateView,
    YouthMemberCreateView, YouthMemberUpdateView, youth_dashboard
)

urlpatterns = [
    # Main page and authentication
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Member area
    path('member/', views.member, name='member'),
    
    # Youth Organization URLs (keep these for functionality)
    path('youth/', YouthOrganizationListView.as_view(), name='youth-organization-list'),
    path('youth/join/', youth_dashboard, name='youth-dashboard'),
    path('youth/org/<int:pk>/', YouthOrganizationDetailView.as_view(), name='youth-organization-detail'),
    
    # Staff-only URLs
    path('youth/org/add/', YouthOrganizationCreateView.as_view(), name='youth-organization-create'),
    path('youth/org/<int:pk>/edit/', YouthOrganizationUpdateView.as_view(), name='youth-organization-update'),
    
    # Member profile URLs
    path('youth/member/add/', YouthMemberCreateView.as_view(), name='youth-member-create'),
    path('youth/member/<int:pk>/edit/', YouthMemberUpdateView.as_view(), name='youth-member-update'),
]
