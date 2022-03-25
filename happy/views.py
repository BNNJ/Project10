
from rest_framework import generics, mixins, viewsets
from django.contrib.auth import get_user_model

from happy.serializers import (
	UserSerializer,
	ProjectSerializer,
	IssueSerializer,
	CommentSerializer,
	ContributorSerializer
)
from happy.models import (
	Project,
	Contributor,
	Issue,
	Comment
)
from happy.permissions import (
	YouShallNotPass,
	IsAuthor,
	IsContributor
)

User = get_user_model()

class ProjectViewSet(viewsets.ModelViewSet):
	queryset = Project.objects.all()
	serializer_class = ProjectSerializer
	permissions = [YouShallNotPass]

	# def filter_queryset(self, queryset):
	# 	return queryset.filter(author=self.request.user.id)

	# def get_queryset(self):
	# 	return Project.objects.all()
	# 	return Project.objects.filter(author=self.request.user.id)

	def perform_create(self, serializer):
		p = serializer.save(author=self.request.user)
		c = Contributor(
			user=self.request.user,
			project=p,
			role="author"
		)
		c.save()

class ContributorViewSet(viewsets.ModelViewSet):
	queryset = Contributor.objects.all()
	serializer_class = ContributorSerializer

class IssueViewSet(viewsets.ModelViewSet):
	queryset = Issue.objects.all()
	serializer_class = IssueSerializer

class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
