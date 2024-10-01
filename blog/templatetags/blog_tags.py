from django import template

register = template.Library()


@register.filter()
def media_blog_filter(path):
    if path:
        return f"/media/{path}"
    return "#"
