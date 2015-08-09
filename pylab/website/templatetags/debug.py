from django import template

register = template.Library()


@register.simple_tag(name='pdb', takes_context=True)
def pdb(context, *args, **kwargs):
    import ipdb; ipdb.set_trace()
