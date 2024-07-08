from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string
from .models import IIIFManifest
import json
from django.contrib import messages
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Funktionert bisher nur auf https://universalviewer.io/
# In diesem Video wird gezeigt, wie man manuell jeden schritt durchgehen kann: https://www.youtube.com/watch?v=u63jHDH3pDM

def index(request):
    if request.method == 'POST':
        manifest = request.POST.get('manifest')
        file = request.FILES.get('file')
        if manifest:
            manifest_data = json.loads(manifest)
            filename = "manifest.json"
            # Convert the manifest data back to a string to save it
            manifest_str = json.dumps(manifest_data)
            # Save the file
            file_name = default_storage.save(filename, ContentFile(manifest_str))
            # Create a IIIFManifest instance
            manifest = IIIFManifest(manifest=manifest_data, filename=filename, file=file_name)
            manifest.save()
        elif file:
            # Read the content of the uploaded file directly
            file_content = file.read().decode('utf-8')  # Assuming the file content is UTF-8 encoded
            manifest_data = json.loads(file_content)
            filename = "manifest.json"  # Generate a unique file name
            # Save the uploaded file
            file_name = default_storage.save(filename, file)
            # Create a IIIFManifest instance
            manifest = IIIFManifest(manifest=manifest_data, filename=filename, file=file_name)
            manifest.save()
        else:
            messages.error(request, 'Kein Manifest oder Datei hochgeladen. Bitte versuchen Sie es erneut.')
            return render(request, 'main/index.html')
        
    return render(request, 'main/index.html')

@api_view(['GET'])
def api_link(request, pk):
    if request.method == 'GET':
        manifest = IIIFManifest.objects.get(pk=pk)
        return Response(manifest.manifest, status=201)
    else:
        return Response(status=400)


def link(request, pk):
    manifest = IIIFManifest.objects.get(pk=pk)
    context = {
        'manifest': manifest
    }
    return render(request, 'main/link.html', context)




    # Now you can work with file_path, which is a path to a temporary file
    # Remember to clean up the temporary file if you created one