from django import forms
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from pylab.core.models import Project, Event


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
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


class NextWeeklyEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'starts', 'ends', 'address', 'osm_map_link', 'description')

    def __init__(self, parent_event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent_event = parent_event

    def check_existing_events(self, title, starts):
        slug = Event._meta.get_field('slug').pre_save(Event(title=title), None)

        qs = Event.objects.filter(
            starts__year=starts.year,
            starts__month=starts.month,
            starts__day=starts.day,
            slug=slug,
        )

        if qs.exists():
            raise forms.ValidationError(ugettext("Event with same title on same day already exist."))

    def clean(self):
        title = self.cleaned_data.get('title')
        starts = self.cleaned_data.get('starts')

        if title and starts:
            self.check_existing_events(title, starts)
