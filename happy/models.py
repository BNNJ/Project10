from django.db import models
from django.contrib.auth import get_user_model

# from django.conf import settings

User = get_user_model()


class Project(models.Model):
    """Project model"""

    BACK = "back"
    FRONT = "front"
    IOS = "ios"
    ANDROID = "android"
    TEST = "test"
    TYPE_CHOICES = [
        (BACK, "backend"),
        (FRONT, "frontend"),
        (IOS, "iOS"),
        (ANDROID, "android"),
        (TEST, "test"),
    ]

    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="created_projects"
    )
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    project_type = models.CharField(max_length=128, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.title} ({self.id})"


class Contributor(models.Model):
    """Contributor model"""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="contributors"
    )
    # permission = models.CharField(max_length=128)
    role = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user} ({self.id}): {self.project} {self.role}"


class Issue(models.Model):
    """Issue model"""

    HI = "high"
    MD = "medium"
    LO = "low"
    PRIORITY_CHOICES = [(HI, "high"), (MD, "medium"), (LO, "low")]

    BUG = "bug"
    IMP = "improvement"
    FEAT = "feature"
    TAG_CHOICES = [(BUG, "bug"), (IMP, "improvement"), (FEAT, "feature")]

    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="created_issues"
    )
    assignee = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="assigned_issues"
    )
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    tag = models.CharField(max_length=128, choices=TAG_CHOICES)
    priority = models.CharField(max_length=128, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(
        to=Project, on_delete=models.CASCADE, related_name="issues"
    )
    status = models.CharField(max_length=128)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.id}) from {self.author} on {self.project}"


class Comment(models.Model):
    """Comment model"""

    issue = models.ForeignKey(
        to=Issue, on_delete=models.CASCADE, related_name="comments"
    )
    description = models.TextField(max_length=2048, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self):
        return f"comment ({self.id}) on {self.issue} from {self.author}"
