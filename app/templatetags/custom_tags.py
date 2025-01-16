from django import template
import datetime
import locale

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def month_year_format(value):
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        date = datetime.datetime.strptime(value, '%Y-%m')
        return date.strftime('%B de %Y').capitalize()
    except ValueError:
        return value