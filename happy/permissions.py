from rest_framework import permissions

from happy.models import Project, Contributor

class IsContributor(permissions.BasePermission):
	""""""

	def has_object_permission(self, request, view, obj):
		if isinstance(obj, Project):
			return request.user.id in Contributor.objects.filter(project=obj.id)
		else:
			return request.user.id in Contributor.objects.filter(project=obj.project.id)

class IsAuthor(permissions.BasePermission):
	""""""

	def has_permission(self, request, view):
		# return request.user.id == obj.author
		return False

	def has_object_permission(self, request, view, obj):
		# return request.user.id == obj.author
		return False

class YouShallNotPass(permissions.BasePermission):
	def has_permission(self, request, view):
		return False
	def has_object_permission(self, request, view, obj):
		return False