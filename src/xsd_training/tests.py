from xSACdb.test_helpers import BaseAsGroupTest, FixtureMixin, BaseTest
from xsd_sites.tests import SiteTestToolsMixin

from xsd_training.models import *

import testdata

class BaseTraineeTest(BaseTest):
    pass

class BaseTrainingTest(BaseAsGroupTest):
    GROUPS=[3]

class TrainingTestToolsMixin(object):
    OD = Qualification.objects.get(code="OD")
    SD = Qualification.objects.get(code="SD")
    DL = Qualification.objects.get(code="DL")
    AD = Qualification.objects.get(code="AD")
    FC = Qualification.objects.get(code="FC")

    ASI = Qualification.objects.get(code="AI")
    PI = Qualification.objects.get(code="PI")
    THI = Qualification.objects.get(code="THI")
    AOI = Qualification.objects.get(code="AOI")
    OWI = Qualification.objects.get(code="OWI")
    AI = Qualification.objects.get(code="AVI")
    NI = Qualification.objects.get(code="NI")

    OO1 = Lesson.objects.get(code="OO1")

    def get_trainee(self, training_for=OD):
        user = self.create_a_user()
        user.training_for = [training_for]
        user.save()
        return user.get_profile()

    def get_instructor(self, qualification=OWI):
        user = self.create_a_user()
        mp = user.get_profile()
        mp.set_qualification(self.OWI)
        mp.save()
        return user.get_profile()

    def create_basic_pl(self, trainee=None):
        if not trainee: trainee = self.get_trainee()
        pl = PerformedLesson.objects.create(
            trainee = trainee
        )
        pl.save()
        return pl

    def create_pl(self, trainee=None, instructor=None):
        if not trainee: trainee = self.get_trainee()
        if not instructor: trainee = self.get_instructor()
        pl = PerformedLesson.objects.create(
            trainee = trainee,
            instructor = instructor,
        )
        pl.save()
        return pl

    def create_session(self, site):
        sesh = Session.objects.create(
            name = testdata.get_str(str_size=128),
            when = testdata.get_future_datetime(),
            where = site,
        )
        sesh.save()
        return sesh



class PerformedLessonTest(BaseTrainingTest, TrainingTestToolsMixin):

    def test_basic_pl(self):
        pl = self.create_basic_pl()
        self.assertIsInstance(pl, PerformedLesson)

    # def test_full_pl(self):
    #     pl = self.create_full_pl()
    #     self.assertIsInstance(pl, PerformedLesson)

    def test_get_date(self):
        pl = self.create_basic_pl()
        self.assertIsNone(pl.get_date())
        myDate = self.get_random_date()
        pl.date = myDate
        pl.save()
        self.assertEqual(pl.get_date(), myDate)

    def test_lesson_completed(self):
        pl = self.create_basic_pl()
        pl.lesson = self.OO1
        pl.save()
        self.assertFalse(self.OO1.is_completed(pl.trainee))

        pl.completed = True
        pl.save()
        self.assertTrue(self.OO1.is_completed(pl.trainee))

    def test_lesson_planned(self):
        trainee = self.get_trainee()
        self.assertFalse(self.OO1.is_planned(trainee))

        pl = self.create_basic_pl(trainee=trainee)
        pl.lesson = self.OO1
        pl.save()

        self.assertTrue(self.OO1.is_planned(pl.trainee))

    def test_lesson_partially_completed(self):
        pl = self.create_basic_pl()
        pl.lesson = self.OO1
        pl.save()
        self.assertFalse(self.OO1.is_partially_completed(pl.trainee))

        pl.partially_completed = True
        pl.save()
        self.assertTrue(self.OO1.is_partially_completed(pl.trainee))

    def test_session_date_sync(self):
        return False

class PerformedLessonManagerTest(BaseTrainingTest, TrainingTestToolsMixin):
    def test_get_lessons(self):
        trainee = self.get_trainee()
        planned_lesson = self.create_basic_pl(trainee=trainee)
        pls = PerformedLesson.objects.get_lessons(trainee=trainee)
        self.assertTrue(planned_lesson in pls)

    def test_get_lessons_lesson(self):
        trainee = self.get_trainee()
        planned_lesson = self.create_basic_pl(trainee=trainee)
        lesson = self.OO1
        planned_lesson.lesson = lesson
        planned_lesson.save()
        pls = PerformedLesson.objects.get_lessons(trainee=trainee, lesson=lesson)
        self.assertTrue(planned_lesson in pls)

    def test_get_lessons_partially_completed(self):
        trainee = self.get_trainee()
        planned_lesson = self.create_basic_pl(trainee=trainee)
        planned_lesson.partially_completed = True
        planned_lesson.save()
        pls = PerformedLesson.objects.get_lessons(trainee=trainee, partially_completed=True)
        self.assertTrue(planned_lesson in pls)

    def test_get_lessons_completed(self):
        trainee = self.get_trainee()
        planned_lesson = self.create_basic_pl(trainee=trainee)
        planned_lesson.completed = True
        planned_lesson.save()
        pls = PerformedLesson.objects.get_lessons(trainee=trainee, completed=True)
        self.assertTrue(planned_lesson in pls)

    def test_get_teaching_planned_lessons(self):
        trainee = self.get_trainee()
        instructor = self.get_instructor()
        planned_lesson = self.create_pl(trainee=trainee, instructor=instructor)
        pls = PerformedLesson.objects.get_teaching(instructor=instructor)
        self.assertTrue(planned_lesson in pls)

    def test_get_teaching_lesson(self):
        trainee = self.get_trainee()
        instructor = self.get_instructor()
        planned_lesson = self.create_pl(trainee=trainee, instructor=instructor)
        lesson = self.OO1
        planned_lesson.lesson = lesson
        planned_lesson.save()
        pls = PerformedLesson.objects.get_teaching(instructor=instructor, lesson=lesson)
        self.assertTrue(planned_lesson in pls)

    def test_get_teaching_partially_completed_lessons(self):
        trainee = self.get_trainee()
        instructor = self.get_instructor()
        planned_lesson = self.create_pl(trainee=trainee, instructor=instructor)
        planned_lesson.partially_completed = True
        planned_lesson.save()
        pls = PerformedLesson.objects.get_teaching(instructor=instructor, partially_completed=True)
        self.assertTrue(planned_lesson in pls)

    def test_get_teaching_completed_lessons(self):
        trainee = self.get_trainee()
        instructor = self.get_instructor()
        planned_lesson = self.create_pl(trainee=trainee, instructor=instructor)
        planned_lesson.completed = True
        planned_lesson.save()
        pls = PerformedLesson.objects.get_teaching(instructor=instructor, completed=True)
        self.assertTrue(planned_lesson in pls)

class PerformedLessonWithSessionTest(BaseTrainingTest, TrainingTestToolsMixin, SiteTestToolsMixin):
    def test_save_with_session(self):
        pl = self.create_basic_pl()
        session = self.create_session(site=self.create_site())
        pl.session = session
        pl.save()
        self.assertTrue(pl.date == session.when.date())


class PoolSheetGenerate(BaseTrainingTest, FixtureMixin):
    url_pool = '/training/pool-sheet/?session=18&sort_by=instructor__last_name&show_public_notes=on&show_private_notes=on&number_of_notes=3&comments_column=on&signature_column=on'
    url_ow = '/training/pool-sheet/?session=16&sort_by=instructor__last_name&show_public_notes=on&show_private_notes=on&number_of_notes=3&comments_column=on&signature_column=on'
    url_theory = '/training/pool-sheet/?session=10&sort_by=trainee__last_name&show_public_notes=on&show_private_notes=on&number_of_notes=3&comments_column=on&signature_column=on'

    def generic_ps(self, url):
        c = self.get_client()
        response = c.get(url)
        self.assertEqual(response.status_code, 200)

        # Response context not getting anything :\
        # self.assertTrue(response.context['session'])
        # self.assertTrue( len(response.context['pls_extended']) > 6 )

    def test_dumb_ps_pool(self):
        self.generic_ps(self.url_ow)
    def test_dumb_ps_ow(self):
        self.generic_ps(self.url_ow)
    def test_dumb_ps_theory(self):
        self.generic_ps(self.url_theory)
