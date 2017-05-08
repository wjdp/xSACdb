from __future__ import unicode_literals

from django.apps import AppConfig
from actstream import registry


class TrainingConfig(AppConfig):
    name = 'xsd_training'
    verbose_name = 'Training'

    def ready(self):
        registry.register(self.get_model('PerformedLesson'))
        registry.register(self.get_model('Lesson'))
        registry.register(self.get_model('PerformedQualification'))
        registry.register(self.get_model('Qualification'))
        registry.register(self.get_model('PerformedSDC'))
        registry.register(self.get_model('SDC'))
        registry.register(self.get_model('Session'))
        registry.register(self.get_model('TraineeGroup'))
