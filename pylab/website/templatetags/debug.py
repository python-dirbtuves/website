import ipdb

from django import template

register = template.Library()


@register.simple_tag(name='pdb', takes_context=True)
def pdb(context, *args, **kwargs):   # pylint: disable=unused-argument
    ipdb.set_trace()
