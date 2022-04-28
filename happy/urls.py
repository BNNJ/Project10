from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedSimpleRouter
from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
)
from happy import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
users_router = NestedSimpleRouter(router, r'projects', lookup='project')
users_router.register(r'users', views.ContributorViewSet, basename='contributors')
issues_router = NestedSimpleRouter(router, r'projects', lookup='project')
issues_router.register(r'issues', views.IssueViewSet, basename='issues')
comments_router = NestedSimpleRouter(issues_router, r'issues', lookup='issue')
comments_router.register(r'comments', views.CommentViewSet, basename='comments')

router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = [
	path('signup/', views.SignupView.as_view(), name='signup'),
	path('login/', TokenObtainPairView.as_view(), name='login'),

	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

	path('', include(router.urls)),
	path('', include(users_router.urls)),
	path('', include(issues_router.urls)),
	path('', include(comments_router.urls))
]
