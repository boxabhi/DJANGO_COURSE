from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, null=True, blank=True,on_delete=models.CASCADE,
                             related_name="post")
    parent = models.ForeignKey('self',null=True,blank=True, on_delete=models.CASCADE, related_name="comments")
    


class Resume(models.Model):
    resume = models.FileField(upload_to="resume")
    skills = models.JSONField(null=True, blank=True)
    total_expericence = models.FloatField(default=1)
    project_category = models.JSONField(null=True , blank=True)


class JobDescription(models.Model):
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
