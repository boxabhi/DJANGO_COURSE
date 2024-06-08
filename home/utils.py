
from django.template.defaultfilters import slugify
import uuid

def generateSlug(name, ModelClass):
    new_slug = slugify(name)
    if ModelClass.objects.filter(slug = new_slug).exists():
        new_slug = f"{new_slug}-{str(uuid.uuid4()).split('-')[0]}"

    return new_slug