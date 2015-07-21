from django import forms
from django.utils.translation import ugettext_lazy as _

import pylab.website.models as website_models


class ProjectForm(forms.ModelForm):
    class Meta:
        model = website_models.Project
        fields = ('title', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 16}),
        }
        help_texts = {
            'description': _(
                "Describe your project idea. You can use "
                "[Markdown](http://daringfireball.net/projects/markdown/syntax){:target=_blank} markup."
            ),
        }
