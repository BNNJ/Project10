from django.db import models
from django.contrib.auth import get_user_model
# from django.conf import settings

User = get_user_model()

class Project(models.Model):
	"""Project model"""
	author = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		related_name="created_projects"
	)
	title = models.CharField(max_length=128)
	description = models.TextField(max_length=2048, blank=True)
	project_type = models.CharField(max_length=128)

	def __str__(self):
		return f"{self.title} ({self.project_type})"

class Contributor(models.Model):
	"""Contributor model"""
	user = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE
	)
	project = models.ForeignKey(
		to=Project,
		on_delete=models.CASCADE,
		related_name="contributors"
	) 
	# permission = models.CharField(max_length=128)
	role = models.CharField(max_length=128)

	def __str__(self):
		return f"{self.user}: {self.project} {self.role}"

class Issue(models.Model):
	"""Issue model"""
	author = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		related_name="created_issues"
	)
	assignee = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		related_name="assigned_issues"
	)
	title = models.CharField(max_length=128)
	description = models.TextField(max_length=2048, blank=True)
	tag = models.CharField(max_length=128)
	priority = models.CharField(max_length=128)
	project = models.ForeignKey(
		to=Project,
		on_delete=models.CASCADE,
		related_name="issues"
	)
	status = models.CharField(max_length=128)
	time_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.title} from {self.author} on {self.project}"

class Comment(models.Model):
	"""Comment model"""
	issue = models.ForeignKey(
		to=Issue,
		on_delete=models.CASCADE,
		related_name="comments"
	)
	description = models.TextField(max_length=2048, blank=True)
	time_created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(
		to=User,
		on_delete=models.CASCADE,
		related_name="comments"
	)

	def __str__(sellf):
		return f"comment on {self.issue} from {self.author}"
