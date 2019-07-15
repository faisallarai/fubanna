import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):

    if new_slug is None:
        slug = slugify(instance.screen_name)
    else:
        slug = new_slug

    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(slug=slug,
                                             randstr=random_string_generator(size=4))
        return unique_slug_generator(instance, new_slug=new_slug)

    return slug
