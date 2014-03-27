from django.db import models
import pafy


class Video(models.Model):
    url = models.URLField()
    youtube_description = models.TextField()

    def __unicode__(self):
        return self.youtube_description

    @models.permalink
    def get_absolute_url(self):
        return ('video', (), {'pk': self.pk})

    def get_pafy_object(self):
        return pafy.new(url=self.url)

    def remove_http(self):
        return self.url.replace('http://youtu.be/', '')