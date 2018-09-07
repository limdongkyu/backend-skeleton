import os
import shutil

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands import startapp


DS_BE_APP_TEMPLATE = 'https://be.skeletons.djangostars.com/djangostars_app_template__django{extensions}.tar.gz'


class Command(startapp.Command):

    def handle(self, **options):
        app_name = options.pop('name')
        target = options.pop('directory')

        directory = os.path.join(settings.BASE_DIR, 'apps', app_name)
        if os.path.exists(directory):
            raise CommandError('App with name "{}" already exists'.format(app_name))

        os.mkdir(directory)

        options['template'] = self.get_template()

        try:
            super(Command, self).handle(name=app_name, directory=directory, **options)
        except CommandError as ex:
            shutil.rmtree(directory)
            raise ex

    @staticmethod
    def get_template():
        extensions = []
        if 'rest_framework' in settings.INSTALLED_APPS:
            extensions.append('drf')

        return DS_BE_APP_TEMPLATE.format(
            extensions='_{}'.format('_'.join(extensions)) if len(extensions) > 0 else ''
        )