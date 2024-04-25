from django.db import models
from users.models import User

class Career(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    salary = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.career.title} by {self.full_name}"