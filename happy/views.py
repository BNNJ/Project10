from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from happy.serializers import (
    UserSerializer,
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
    ContributorSerializer,
)
from happy.models import Project, Contributor, Issue, Comment
from happy.permissions import IsAuthor, IsContributor

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = [
            c.project
            for c in Contributor.objects.filter(user=self.request.user).select_related(
                "project"
            )
        ]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        p = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=p, role="author")

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            self.permission_classes = [IsAuthenticated & IsAuthor]
        elif self.action in ["create", "list"]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated & IsContributor]
        return super().get_permissions()


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs.get("project_pk"))

    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.POST.get("user"))
        project = Project.objects.get(id=self.kwargs.get("project_pk"))
        serializer.save(project=project, user=user)

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            self.permission_classes = [IsAuthenticated & IsAuthor]
        else:
            self.permission_classes = [IsAuthenticated & IsContributor]
        return super().get_permissions()


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs.get("project_pk"))

    def perform_create(self, serializer):
        assignee_id = self.request.POST.get("assignee")
        if assignee_id is not None:
            assignee = Contributor.objects.get(id=assignee_id)
        else:
            assignee = self.request.user
        project = Project.objects.get(id=self.kwargs.get("project_pk"))
        serializer.save(author=self.request.user, assignee=assignee, project=project)

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            self.permission_classes = [IsAuthenticated & IsAuthor]
        else:
            self.permission_classes = [IsAuthenticated & IsContributor]
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs.get("issue_pk"))

    def perform_create(self, serializer):
        issue = Issue.objects.get(id=self.kwargs.get("issue_pk"))
        serializer.save(issue=issue, author=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "destroy"]:
            self.permission_classes = [IsAuthenticated & IsAuthor]
        else:
            self.permission_classes = [IsAuthenticated & IsContributor]
        return super().get_permissions()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
