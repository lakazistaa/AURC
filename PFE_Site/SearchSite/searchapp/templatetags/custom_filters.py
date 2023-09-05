from django import template

register = template.Library()

@register.filter
def extract_year(value):
    
    try:
        year = str(value).removesuffix('.0')
        return year
    except (ValueError, AttributeError):
        return value
