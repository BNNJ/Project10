from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
)
from happy import views

router = DefaultRouter()
router.register(r'', views.ProjectViewSet)
router.register(r'<int:project_id>/users', views.ContributorViewSet)
router.register(r'<int:project_id>/issues', views.IssueViewSet)
router.register(r'<int:project_id>/issues/<int:issue_id>/comments', views.CommentViewSet)

urlpatterns = [
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

	path('users/', views.UserListView.as_view()),

	path('projects/', include(router.urls))
]
