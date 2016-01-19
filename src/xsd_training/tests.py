from xSACdb.test_helpers import BaseAsGroupTest, BaseTest
from xsd_sites.tests import SiteTestToolsMixin

from xsd_training.models import *

import testdata

class BaseTraineeTest(BaseTest):
    pass

class BaseTrainingTest(BaseAsGroupTest):
    GROUPS=[3]

class TrainingTestToolsMixin(object):

    def trainingTestToolsSetUp(self):
        self.OD = Qualification.objects.get(code="OD")
        self.SD = Qualification.objects.get(code="SD")
        self.DL = Qualification.objects.get(code="DL")
        self.AD = Qualification.objects.get(code="AD")
        self.FC = Qualification.objects.get(code="FC")

        self.PERSONAL_QUALS = [self.OD, self.SD, self.DL, self.AD, self.FC]

        self.ASI = Qualification.objects.get(code="AI")
        self.PI = Qualification.objects.get(code="PI")
        self.THI = Qualification.objects.get(code="THI")
        self.AOI = Qualification.objects.get(code="AOI")
        self.OWI = Qualification.objects.get(code="OWI")
        self.AI = Qualification.objects.get(code="AVI")
        self.NI = Qualification.objects.get(code="NI")

        self.INSTRUCTOR_QUALS = [self.ASI, self.PI, self.THI, self.AOI, self.OWI,
            self.AI, self.NI]

        self.OO1 = Lesson.objects.get(code="OO1")
        self.SO1 = Lesson.objects.get(code="SO1")

        self.BOAT_HANDLING = SDC.objects.get(title="Boat Handling")
        self.WRECK_APPRECIATION = SDC.objects.get(title="Wreck Appreciation")

    def get_trainee(self, training_for=None):
        if not training_for: training_for=self.OD
        user = self.create_a_user()
        user.training_for = [training_for]
        user.save()
        return user.get_profile()

    def get_instructor(self, qualification=None):
        if not qualification: qualification=self.OWI
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
    def setUp(self):
        self.trainingTestToolsSetUp()

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
    def setUp(self):
        self.trainingTestToolsSetUp()

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
    def setUp(self):
        self.trainingTestToolsSetUp()

    def test_save_with_session(self):
        pl = self.create_basic_pl()
        session = self.create_session(site=self.create_site())
        pl.session = session
        pl.save()
        self.assertTrue(pl.date == session.when.date())

class LessonTest(BaseTrainingTest, TrainingTestToolsMixin):
    def setUp(self):
        self.trainingTestToolsSetUp()

    def test_unicode(self):
        lesson = self.OO1
        self.assertTrue(lesson.code in unicode(lesson))
        self.assertTrue(lesson.title in unicode(lesson))

class QualificationTest(BaseTrainingTest, TrainingTestToolsMixin):
    def setUp(self):
        self.trainingTestToolsSetUp()

    def test_lessons_by_mode(self):
        mode = "TH"
        lessons = self.OD.lessons_by_mode(mode=mode)
        self.assertTrue(len(lessons) == 7)

class PerformedSDCTest(BaseTraineeTest, TrainingTestToolsMixin):
    def setUp(self):
        self.trainingTestToolsSetUp()

    def test_get_absolute_url(self):
        psdc = PerformedSDC.objects.create(
            sdc = SDC.objects.all()[0], # Lazily get the first SDC from BSAC data
            datetime = self.get_random_date(),
        )
        psdc.save()
        psdc.trainees.add(self.get_trainee(), self.get_trainee())
        self.assertIsInstance(psdc.get_absolute_url(), basestring)

class SessionTest(BaseTraineeTest, TrainingTestToolsMixin, SiteTestToolsMixin):
    def setUp(self):
        self.trainingTestToolsSetUp()

    def test_complete(self):
        sesh = self.create_session(site=self.create_site())
        sesh.completed = True
        sesh.save()
        self.assertTrue(sesh.completed)

    def test_in_past(self):
        future_sesh = Session.objects.create(
            name = testdata.get_str(str_size=128),
            when = testdata.get_future_datetime(),
            where = self.create_site(),
        )
        future_sesh.save()
        past_sesh = Session.objects.create(
            name = testdata.get_str(str_size=128),
            when = testdata.get_past_datetime(),
            where = self.create_site(),
        )
        past_sesh.save()
        self.assertFalse(future_sesh.in_past())
        self.assertTrue(past_sesh.in_past())

    def test_get_absolute_url(self):
        sesh = self.create_session(site=self.create_site())
        self.assertIsInstance(sesh.get_absolute_url(), basestring)

    def test_unicode(self):
        sesh = Session.objects.create(
            when = self.get_random_date(),
            where = self.create_site()
        )
        self.assertIsInstance(unicode(sesh), basestring)
        self.assertTrue(len(unicode(sesh)) > 5)
        sesh.name = "SuperSession"
        sesh.save()
        self.assertIsInstance(unicode(sesh), basestring)
        self.assertTrue(len(unicode(sesh)) > 5)
        self.assertTrue("SuperSession" in unicode(sesh))

class TraineeGroupTest(BaseTraineeTest, TrainingTestToolsMixin):
    def setUp(self):
        self.trainingTestToolsSetUp()

    def test_trainees_list(self):
        trainee1 = self.get_trainee()
        trainee2 = self.get_trainee()
        tg = TraineeGroup.objects.create()
        tg.save()
        tg.trainees.add(trainee1, trainee2)

        self.assertIsInstance(tg.trainees_list(), basestring)
        self.assertTrue(trainee1.get_full_name() in tg.trainees_list())
        self.assertTrue(trainee2.get_full_name() in tg.trainees_list())

    def test_trainees_list_with_links(self):
        trainee1 = self.get_trainee()
        trainee2 = self.get_trainee()
        tg = TraineeGroup.objects.create()
        tg.save()
        tg.trainees.add(trainee1, trainee2)

        self.assertIsInstance(tg.trainees_list(), basestring)
        self.assertTrue(trainee1.get_full_name() in tg.trainees_list())
        self.assertTrue(trainee2.get_full_name() in tg.trainees_list())
        self.assertTrue("<a href=" in tg.trainees_list_with_links())

    def test_get_all_trainees(self):
        trainee1 = self.get_trainee()
        trainee2 = self.get_trainee()
        tg = TraineeGroup.objects.create()
        tg.save()
        tg.trainees.add(trainee1, trainee2)

        self.assertTrue(trainee1 in tg.get_all_trainees())
        self.assertTrue(trainee2 in tg.get_all_trainees())

    def test_unicode(self):
        name = testdata.get_str(128)
        tg = TraineeGroup.objects.create(name=name)
        tg.save()

        self.assertEqual(unicode(tg), name)



class PoolSheetGenerate(BaseTrainingTest):
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
