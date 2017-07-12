from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=True)
def name_joins(value, arg):
	''' join the attributes of object '''

	comma_string = None;
	for val in value.all():
		if comma_string is not None:
			comma_string = comma_string + ", " +str(val)
		else:
			comma_string = str(val)

	return comma_string
