import math
from django import template

register = template.Library()

@register.filter
def split_to_columns(queryset, rows):
    values = list(queryset.all())
    columns = int(math.ceil(float(len(values)) / rows))
    result = [values[i * rows:(i + 1) * rows] for i in range(columns)]
    return result
