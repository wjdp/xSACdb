from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db import transaction
from reversion import revisions as reversion


@reversion.register()
class TraineeGroup(models.Model):
    name = models.CharField(max_length=64, unique=True)
    trainees = models.ManyToManyField(settings.AUTH_PROFILE_MODEL, blank=True)

    TRAINEE_ORDER_BY = 'last_name'

    def __unicode__(self):
        return "{} {}".format(self.uid(), self.name)

    def uid(self):
        return "TG{:0>4d}".format(self.pk)

    def trainees_list(self):
        """returns a readable list of trainee full names separated by commas"""
        ret = ""
        for t in self.trainees.all().order_by(self.TRAINEE_ORDER_BY):
            ret = ret + t.get_full_name() + ", "

        # chop off trailing comma
        return ret[:-2]

    def trainees_list_with_links(self):
        ret = ''
        for t in self.trainees.all().order_by(self.TRAINEE_ORDER_BY):
            ret += '<a href=\"' + reverse('xsd_training:TraineeNotes', kwargs={'pk': t.pk}) + '\">' + \
                   t.get_full_name() + '</a>, '
        return ret[:-2]

    def add_trainees(self, trainees):
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Added trainees')
            existing_trainees = self.trainees.all()
            for trainee in trainees:
                if trainee not in existing_trainees:
                    self.trainees.add(trainee)
            self.save()

    def remove_trainees(self, trainees):
        with reversion.create_revision() and transaction.atomic():
            if reversion.is_active():
                reversion.set_comment('Removed trainees')
            for trainee in trainees:
                self.trainees.remove(trainee)
            self.save()

    def get_all_trainees(self):
        return self.trainees.all().order_by(self.TRAINEE_ORDER_BY)

    def get_absolute_url(self):
        return reverse('xsd_training:TraineeGroupUpdate', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']
