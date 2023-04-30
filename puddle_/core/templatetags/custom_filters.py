from django import template

register = template.Library()

@register.filter
def chunkify(items, chunk_size):
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

