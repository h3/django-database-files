import base64
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_control
import mimetypes
from database_files.models import File
import os
import StringIO

from django.views import static

#@cache_control(max_age=86400)
def serve(request, name, **kwargs):
    file_path = os.path.join(settings.MEDIA_ROOT, name)
    if not os.path.exists(file_path):
        print "Saving %s" % file_path
        try:
            f = File.objects.get(name=name)
        except File.DoesNotExist:
            return None
        with open(file_path, 'wb') as fh:
            fh.write(base64.b64decode(f.content))

    return static.serve(request, name, **kwargs)


#       f = get_object_or_404(File, name=name)
#       mimetype = mimetypes.guess_type(name)[0] or 'application/octet-stream'
#       response = HttpResponse(base64.b64decode(f.content), mimetype=mimetype)
#       response['Content-Length'] = f.size
#       return response
