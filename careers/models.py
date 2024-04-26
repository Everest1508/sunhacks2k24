from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from .find_resume_score import calculate_score

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
    score = models.FloatField(null=True,blank=True,)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application for {self.career.title} by {self.user.name}"
    
    
@receiver(post_save, sender=Application)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        instance.score = float(calculate_score(cv_file=instance.resume,jd_file=instance.career.description))
        instance.save()