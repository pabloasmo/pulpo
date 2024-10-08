from django.db import models
from django.contrib.auth.models import User

class ContentType(models.Model):
    name = models.CharField(max_length=100)
    source = models.ForeignKey('Source', related_name='content_types', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=50, unique=True)
    docs_url = models.URLField(null=True, blank=True)
    endpoint_url = models.URLField()

    def __str__(self):
        return self.name

class Content(models.Model):
    content_type = models.ForeignKey(ContentType, related_name='contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    external_id = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    rating = models.TextField(null=True, blank=True)
    cover_image = models.URLField(null=True, blank=True)
    genres = models.ManyToManyField('Genre', related_name='contents', blank=True)

    class Meta:
        unique_together = ('content_type', 'external_id')

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserContent(models.Model):
    STATUS_CHOICES = [
        ('PL', 'Plan to Watch/Read/Listen'),
        ('WT', 'Watching/Reading/Listening'),
        ('CM', 'Completed'),
    ]
    user = models.ForeignKey(User, related_name='user_contents', on_delete=models.CASCADE)
    content = models.ForeignKey(Content, related_name='user_content', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PL')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'content')

    def __str__(self):
        return f'{self.user} - {self.content.title}'