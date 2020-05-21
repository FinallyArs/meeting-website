from django import template
register = template.Library()


@register.simple_tag
def get_second_user(user, chat):
    for u in chat.members.all():
        if u != user:
            return u
    return None
