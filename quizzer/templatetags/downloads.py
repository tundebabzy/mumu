from django import template
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse

__author__ = 'tunde'

register = template.Library()


@register.tag(name='files')
def get_downloads(parser, token):
    try:
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'Tag takes no argument'
        )
    return NavigationNode()


class NavigationNode(template.Node):
    """
    Check downloads folder in STATIC_ROOT first or fall back to STATICFILES_DIR.
    Generate HTML using folder name as header
    """

    def render(self, context):
        return self.get_html_code(context)

    def get_html_code(self, context):
        file_storage = FileSystemStorage(location=settings.STATICFILES_DIRS[0], base_url=settings.STATIC_URL)
        if not file_storage.exists('downloads') or not file_storage.listdir('downloads')[0]:
            # note: listdir returns a tuple:- (directory, files). We wish to use folders as headings and the files in
            # the sub folders for links, if the download folder has only files without folders, we ignore them because
            # they will not be used
            return self.empty_html_message()

        return self.build_html(file_storage)

    def build_html(self, file_storage):
        file_storage = file_storage
        html = "<dl>"
        for directory in file_storage.listdir('downloads')[0]:
            ns = '<dt>%s</dt>' % directory.replace('_', ' ').title()
            html += ns
            for file in file_storage.listdir('downloads/' + directory + '/')[1]:
                ns = '<dd><a href="%s">%s</a></dd>' % (reverse('download_link',kwargs={'pdfname': file}),
                                                       file.replace('-', ' '))
                html += ns
        html += '</dl>'
        return html


    def empty_html_message(self):
        return "<p>Nothing here <strong>YET</strong></p>"