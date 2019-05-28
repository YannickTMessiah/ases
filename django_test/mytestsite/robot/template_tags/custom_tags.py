from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# https://stackoverflow.com/questions/50703556/get-dictionary-value-by-key-in-django-template