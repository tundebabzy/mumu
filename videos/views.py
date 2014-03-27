from django.views.generic import ListView, DetailView, View
from django import http
from videos.models import Video
import pafy


class ListVideos(ListView):
    paginate_by = 10
    http_method_names = ['get']
    model = Video
    template_name = 'videos_video_list.html'

class DetailVideo(DetailView):
    model = Video
    context_object_name = 'video'
    template_name_field = 'video'