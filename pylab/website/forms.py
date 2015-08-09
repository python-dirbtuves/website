import datetime

from django import forms
from django.forms.models import BaseModelFormSet
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from pylab.core.models import Project, Event, Vote


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


class VotePointsForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('points',)
        widgets = {
            'points': forms.NumberInput(attrs={'max': 99, 'class': 'vote-points-input'}),
        }

    def save(self, commit=True, *args, **kwargs):
        vote = super(VotePointsForm, self).save(commit=False, *args, **kwargs)
        vote.voted = datetime.datetime.now()
        vote.save()


class BaseTotalPointsFormset(BaseModelFormSet):
    def clean(self, *args, **kwargs):
        super(BaseTotalPointsFormset, self).clean(*args, **kwargs)
        total_points = 0

        for form in self.forms:
            if form.cleaned_data['points']:
                total_points += form.cleaned_data['points']

        if total_points < 0 or total_points > 15:
            raise forms.ValidationError(ugettext(
                "Sum of voting points is out of bounds. Expected from 0 to 15, but got %s."
            ) % total_points)
