import base64
from database_files import models
from django.conf import settings
from django.db import IntegrityError
from django.core import files
from django.core.files.storage import Storage
from django.core.urlresolvers import reverse
import os
import StringIO

class DatabaseStorage(Storage):
    _path = False
    def _generate_name(self, name, pk):
        """
        Replaces the filename with the specified pk and removes any dir
        """
        self._path = name
        dir_name, file_name = os.path.split(name)
       #file_root, file_ext = os.path.splitext(file_name)
        return file_name

    def path(self, name):
        if self._path:
            return self._path
        self._path = name
        return name
    
    def _open(self, name, mode='rb'):
        try:
            f = models.File.objects.get(name=name)
        except models.File.DoesNotExist:
            return None
        fh = StringIO.StringIO(base64.b64decode(f.content))
        fh.name = name
        fh.mode = mode
        fh.size = f.size
        return files.File(fh)
    
    def _save(self, name, content):
        try:
            f = models.File.objects.create(
                name=name,
                content=base64.b64encode(content.read()),
                size=content.size,
            )
        except IntegrityError:
            # Updating existing image
            f = models.File.objects.get(name=name)
            f.content = base64.b64encode(content.read())
            f.size = content.size
            f.save()

        return name
    
    def exists(self, name):
        """
        We overwrite existing files in db, so no need to check if it exists
        """
        return False
    
    def delete(self, name):
        try:
            models.File.objects.get_from_name(name).delete()
        except models.File.DoesNotExist:
            pass
    
    def url(self, name):
        return os.path.join(settings.MEDIA_URL, name)
        #return reverse('database_file', kwargs={'name': name})
    
    def size(self, name):
        try:
            return models.File.objects.get_from_name(name).size
        except models.File.DoesNotExist:
            return 0

