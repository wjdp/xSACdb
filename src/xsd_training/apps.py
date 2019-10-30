

from django.apps import AppConfig


class TrainingConfig(AppConfig):
    name = 'xsd_training'
    verbose_name = 'Training'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('PerformedLesson'))
        registry.register(self.get_model('Lesson'))
        registry.register(self.get_model('PerformedQualification'))
        registry.register(self.get_model('Qualification'))
        registry.register(self.get_model('PerformedSDC'))
        registry.register(self.get_model('SDC'))
        registry.register(self.get_model('Session'))
        registry.register(self.get_model('TraineeGroup'))
