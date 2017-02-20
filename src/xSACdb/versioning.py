from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.db.models import IntegerField, EmailField, TextField
from django.db.models.loading import get_model
from django.conf import settings

import reversion
import diff_match_patch

def model_compare(oldObj, newObj, excluded_keys=[]):
    # Receives two objects of the same model, and compares them. Returns an array of FieldCompare objects
    try:
        theFields = oldObj._meta.fields  # This becomes deprecated in Django 1.8!!!!!!!!!!!!! (but an alternative becomes available)
    except AttributeError:
        theFields = newObj._meta.fields

    class FieldCompare(object):
        def __init__(self, field=None, old=None, new=None):
            self.field = field
            self._old = old
            self._new = new

        def display_value(self, value):
            if isinstance(self.field, IntegerField) and len(self.field.choices) > 0:
                return [x[1] for x in self.field.choices if x[0] == value][0]
            return value

        @property
        def old(self):
            return self.display_value(self._old)

        @property
        def new(self):
            return self.display_value(self._new)

        @property
        def long(self):
            if isinstance(self.field, EmailField):
                return True
            return False

        @property
        def linebreaks(self):
            if isinstance(self.field, TextField):
                return True
            return False

        @property
        def diff(self):
            oldText = unicode(self.display_value(self._old)) or ""
            newText = unicode(self.display_value(self._new)) or ""
            dmp = diff_match_patch()
            diffs = dmp.diff_main(oldText, newText)
            dmp.diff_cleanupSemantic(diffs)

            outputDiffs = []

            for (op, data) in diffs:
                if op == dmp.DIFF_INSERT:
                    outputDiffs.append({'type': 'insert', 'text': data})
                elif op == dmp.DIFF_DELETE:
                    outputDiffs.append({'type': 'delete', 'text': data})
                elif op == dmp.DIFF_EQUAL:
                    outputDiffs.append({'type': 'equal', 'text': data})
            return outputDiffs

    changes = []

    for thisField in theFields:
        name = thisField.name

        if name in excluded_keys:
            continue  # if we're excluding this field, skip over it

        try:
            oldValue = getattr(oldObj, name, None)
        except ObjectDoesNotExist:
            oldValue = None

        try:
            newValue = getattr(newObj, name, None)
        except ObjectDoesNotExist:
            newValue = None

        try:
            bothBlank = (not oldValue) and (not newValue)
            if oldValue != newValue and not bothBlank:
                compare = FieldCompare(thisField, oldValue, newValue)
                changes.append(compare)
        except TypeError:  # logs issues with naive vs tz-aware datetimes
            logger.error('TypeError when comparing models')

    return changes

def get_versions_for_model(models):
    content_types = []
    for model in models:
        content_types.append(ContentType.objects.get_for_model(model))

    versions = reversion.models.Version.objects.filter(
        content_type__in=content_types,
    ).select_related("revision").order_by("-pk")

    return versions

def get_previous_version(version):
    thisId = version.object_id
    thisVersionId = version.pk

    versions = reversion.revisions.get_for_object_reference(version.content_type.model_class(), thisId)

    try:
        previousVersions = versions.filter(revision_id__lt=version.revision_id).latest(
            field_name='revision__date_created')
    except ObjectDoesNotExist:
        return False

    return previousVersions

def get_changes_for_version(newVersion, oldVersion=None):
    # Pass in a previous version if you already know it (for efficiency)
    # if not provided then it will be looked up in the database

    if oldVersion == None:
        oldVersion = get_previous_version(newVersion)

    modelClass = newVersion.content_type.model_class()

    compare = {
        'revision': newVersion.revision,
        'new': newVersion.object_version.object,
        'current': modelClass.objects.filter(pk=newVersion.pk).first(),
        'version': newVersion,

        # Old things that may not be used
        'old': None,
        'field_changes': None,
        'item_changes': None,
    }

    if oldVersion:
        compare['old'] = oldVersion.object_version.object
        compare['field_changes'] = model_compare(compare['old'], compare['new'])
        #compare['item_changes'] = compare_event_items(oldVersion, newVersion)

    return compare

def get_activity_feed_models():
    # Interprets the ACTIVITY_MODELS setting
    models = []
    for modelTuple in settings.ACTIVITY_MODELS:
        models.append(get_model(modelTuple[0], modelTuple[1]))
    return models
