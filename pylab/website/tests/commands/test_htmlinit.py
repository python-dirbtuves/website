import mock

from django.test import TestCase
from django.utils.six import StringIO
from django.core.management.base import CommandError
from django.core.management import call_command


class HtmlLintCommandTests(TestCase):

    @mock.patch('pylab.website.management.commands.htmllint.get_templates')
    def test_command_output(self, get_templates):
        template = mock.MagicMock()
        template.open = mock.mock_open(read_data='<div><p>foo bar</p></div>')
        template.__str__.return_value = 'foobar.html'
        get_templates.return_value = [template]

        out = StringIO()
        self.assertRaises(CommandError, call_command, 'htmllint', stdout=out)
        self.assertEquals(out.getvalue().splitlines()[:2], [
            '  File "foobar.html", line 1, in <template>',
            '    <div><p>foo bar</p></div>',
        ])
