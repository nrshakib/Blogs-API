from django.conf import settings
from django.db import models
from django.utils.text import slugify

class PostModel(models.Model):
    class StatusChoice(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True, default='')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'posts'
    )
    status = models.CharField(max_length=10, choices=StatusChoice.choices, default=StatusChoice.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # create unique slug
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug=base_slug
            counter = 2

            while PostModel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title