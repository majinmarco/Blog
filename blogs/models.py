from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
	"""A blog started by a user"""
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	public = models.BooleanField(default=False)

	def __str__(self):
		"""Return a string representation of the model"""
		return self.text

class Post(models.Model):
	"""A post within a blog created by a user!"""
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		"""Return a string representation of the model."""
		return f"{self.text[:50]}..."