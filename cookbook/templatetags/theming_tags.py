from django import template
from django.templatetags.static import static

from cookbook.models import UserPreference
from recipes.settings import STICKY_NAV_PREF_DEFAULT

register = template.Library()


@register.simple_tag
def theme_url(request):
    if not request.user.is_authenticated:
        return static('themes/tandoor.min.css')
    themes = {
        UserPreference.BOOTSTRAP: 'themes/bootstrap.min.css',
        UserPreference.FLATLY: 'themes/flatly.min.css',
        UserPreference.DARKLY: 'themes/darkly.min.css',
        UserPreference.SUPERHERO: 'themes/superhero.min.css',
        UserPreference.TANDOOR: 'themes/tandoor.min.css',
        UserPreference.TANDOOR_DARK: 'themes/tandoor_dark.min.css',
    }
    if request.user.userpreference.theme in themes:
        return static(themes[request.user.userpreference.theme])
    else:
        raise AttributeError


@register.simple_tag
def nav_color(request):
    if not request.user.is_authenticated:
        return 'navbar-light bg-primary'

    if request.user.userpreference.nav_color.lower() in ['light', 'warning', 'info', 'success']:
        return f'navbar-light bg-{request.user.userpreference.nav_color.lower()}'
    else:
        return f'navbar-dark bg-{request.user.userpreference.nav_color.lower()}'


@register.simple_tag
def sticky_nav(request):
    if (not request.user.is_authenticated and STICKY_NAV_PREF_DEFAULT) or \
            (request.user.is_authenticated and request.user.userpreference.sticky_navbar):  # noqa: E501
        return 'position: sticky; top: 0; left: 0; z-index: 1000;'
    else:
        return ''
