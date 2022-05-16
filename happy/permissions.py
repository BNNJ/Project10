from rest_framework import permissions

from happy.models import Project, Contributor


class IsSuperuser(permissions.BasePermission):

	def has_permission(self, request, view):
		return request.user.is_superuser()

	def has_object_permission(self, request, view, obj):
		return request.user.is_superuser()

class IsAuthor(permissions.BasePermission):
	""""""
	message = "Only the author has access to this."

	def has_permission(self, request, view):
		return True

	def has_object_permission(self, request, view, obj):
		if isinstance(obj, Contributor):
			return request.user.id == obj.project.author.id
		else:
			return request.user.id == obj.author.id

class IsContributor(permissions.BasePermission):
	"""Allow access only to a project's contributor"""
	message = "You need to be a contributor to this project to do this."

	def has_permission(self, request, view):
		project_id = view.kwargs.get('project_pk', view.kwargs.get('pk'))
		contributors = [c.user for c in Contributor.objects.filter(project_id=project_id)]
		return request.user in contributors

	def has_object_permission(self, request, view, obj):
		return True

class YouShallNotPass(permissions.BasePermission):
	def has_permission(self, request, view):
		return False
	def has_object_permission(self, request, view, obj):
		return False