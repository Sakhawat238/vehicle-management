from django import template
from adminsite.usermanagement.models import USER_TYPE, User



register = template.Library()

@register.inclusion_tag('templatetags/navbarright.html')
def profile_load(requests):
    userObj = requests.user
    loggedin = not userObj.is_anonymous
    return {
        'loggedin': loggedin,
        'type': userObj.type if loggedin else "",
        'id': userObj.id if loggedin else ""
    }