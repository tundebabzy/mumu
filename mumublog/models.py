from django.db import models
from django.utils.text import slugify
from registration.models import RegistrationProfile


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.CharField(max_length=100, default='')
    text = models.TextField()
    approved = models.BooleanField()
    created_by = models.ForeignKey(RegistrationProfile)
    created_on = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('article', (), {'slug':self.slug})