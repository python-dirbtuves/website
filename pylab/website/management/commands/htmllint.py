import html_linter
import template_remover

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


def get_templates():  # pragma: no cover
    return (settings.PROJECT_DIR / 'pylab').glob('**/templates/**/*.html')


class Command(BaseCommand):
    help = 'Lint html templates'

    def handle(self, *args, **options):
        errors_found = 0

        for template in get_templates():
            with template.open() as f:
                content = f.read()

            content = template_remover.clean(content)

            exclude = (
                html_linter.ProtocolMessage,
                html_linter.TypeAttributeMessage,
                html_linter.ExtraWhitespaceMessage,
            )

            lines = content.splitlines()
            levels = {'Error', 'Warning'}
            result = html_linter.HTML5Linter(content)
            for message in result.messages:
                if message.level in levels and not isinstance(message, exclude):
                    self.stdout.write('  File "%s", line %d, in <template>' % (template, message.line))
                    self.stdout.write('    %s' % lines[message.line - 1].strip())
                    self.stdout.write('%s: %s: %s: %s' % (
                        message.level, message.category, message.description, message.message,
                    ))
                    self.stdout.write('')

                    errors_found += 1

        if errors_found > 0:
            raise CommandError('Number of errors found: %d.' % errors_found)
