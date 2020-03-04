

from xsd_sites.tests import SiteTestToolsMixin
from .base import *


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

    def test_pl_set_training_for(self):
        # If the user doesn't have their training_for set, creating a PL should do this
        trainee = self.create_a_user().memberprofile
        # New member should have no training_for
        self.assertEqual(trainee.training_for, None)
        pl = self.create_basic_pl(trainee)
        pl.save()
        # PL was blank, still no training_for
        self.assertEqual(trainee.training_for, None)
        pl = self.create_basic_pl(trainee)
        pl.lesson = self.OO1
        pl.save()
        # Now we have an OD lesson, should reflect
        self.assertEqual(trainee.training_for, self.OD)
        pl = self.create_basic_pl(trainee)
        pl.lesson = self.SO1
        pl.save()
        # SD lesson added, again reflect
        self.assertEqual(trainee.training_for, self.SD)
        pl = self.create_basic_pl(trainee)
        pl.lesson = self.OO2
        pl.completed = True
        pl.save()
        # Add another OD and complete it, is lower ranked so should not change
        self.assertEqual(trainee.training_for, self.SD)

    def test_pl_trainee_permissions(self):
        pl = self.create_basic_pl()
        user = pl.trainee.user
        self.assertTrue(pl.permissions.can_view(user))
        self.assertFalse(pl.permissions.can_view_private(user))
        self.assertFalse(pl.permissions.can_edit(user))
        self.assertFalse(pl.permissions.can_delete(user))

    def test_pl_instructor_permissions(self):
        pl = self.create_pl()
        user = pl.instructor.user
        self.assertTrue(pl.permissions.can_view(user))
        self.assertTrue(pl.permissions.can_view_private(user))
        self.assertTrue(pl.permissions.can_edit(user))
        self.assertTrue(pl.permissions.can_delete(user))

    def test_pl_other_instructor_permissions(self):
        pl = self.create_pl()
        user = self.get_instructor().user
        self.assertTrue(pl.permissions.can_view(user))
        self.assertTrue(pl.permissions.can_view_private(user))
        self.assertFalse(pl.permissions.can_edit(user))
        self.assertFalse(pl.permissions.can_delete(user))

    def test_pl_training_officer_permissions(self):
        pl = self.create_pl()
        user = self.get_training_officer().user
        self.assertTrue(pl.permissions.can_view(user))
        self.assertTrue(pl.permissions.can_view_private(user))
        self.assertTrue(pl.permissions.can_edit(user))
        self.assertTrue(pl.permissions.can_delete(user))


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
        self.assertTrue(lesson.code in str(lesson))
        self.assertTrue(lesson.title in str(lesson))


class QualificationTest(BaseTrainingTest, TrainingTestToolsMixin):
    def setUp(self):
        self.trainingTestToolsSetUp()

    def test_lessons_by_mode(self):
        mode = "TH"
        lessons = self.OD.lessons_by_mode(mode=mode)
        self.assertTrue(len(lessons) == 6)


class QualificationManagerTest(BaseTrainingTest, TrainingTestToolsMixin):
    def setUp(self):
        self.trainingTestToolsSetUp()

    def test_get_active(self):
        quals = Qualification.objects.get_active()
        # checking directly results in different objects, just check count and that our excluded one isn't in there
        self.assertCountEqual(self.ACTIVE_QUALS, quals)
        self.assertNotIn(self.ODL, quals)

    def test_get_active_training_for(self):
        trainee = self.get_trainee(self.ODL)
        trainee.training_for = self.ODL
        trainee.save()

        quals = Qualification.objects.get_active(trainee)
        self.assertIn(self.ODL, quals)

    def test_get_active_completed(self):
        trainee = self.get_instructor(self.ODL) # sets the current qualification correctly

        quals = Qualification.objects.get_active(trainee)
        self.assertIn(self.ODL, quals)

    def test_get_active_with_pl(self):
        pl = self.create_basic_pl()
        pl.lesson = Lesson.objects.get(code="OO1", qualification=self.ODL)
        pl.save()

        quals = Qualification.objects.get_active(pl.trainee)
        self.assertIn(self.ODL, quals)

    def test_excluded_by_rank(self):
        trainee = self.get_trainee(self.ODL)
        trainee.training_for = self.ODL
        trainee.save()

        quals = Qualification.objects.get_active(trainee)
        self.assertNotIn(self.OD, quals)

# TODO Award Qualifications

class PerformedSDCTest(BaseTraineeTest, TrainingTestToolsMixin):
    def setUp(self):
        self.trainingTestToolsSetUp()

    def test_get_absolute_url(self):
        psdc = PerformedSDC.objects.create(
            sdc=SDC.objects.all()[0],  # Lazily get the first SDC from BSAC data
            datetime=self.get_random_date(),
        )
        psdc.save()
        psdc.trainees.add(self.get_trainee(), self.get_trainee())
        self.assertIsInstance(psdc.get_absolute_url(), str)


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
            name=self.fake.name(),
            when=self.get_future_datetime(),
            where=self.create_site(),
        )
        future_sesh.save()
        past_sesh = Session.objects.create(
            name=self.fake.name(),
            when=self.get_past_datetime(),
            where=self.create_site(),
        )
        past_sesh.save()
        self.assertFalse(future_sesh.in_past())
        self.assertTrue(past_sesh.in_past())

    def test_get_absolute_url(self):
        sesh = self.create_session(site=self.create_site())
        self.assertIsInstance(sesh.get_absolute_url(), str)

    def test_unicode(self):
        sesh = Session.objects.create(
            when=self.get_random_date(),
            where=self.create_site()
        )
        self.assertIsInstance(str(sesh), str)
        self.assertTrue(len(str(sesh)) > 5)
        sesh.name = "SuperSession"
        sesh.save()
        self.assertIsInstance(str(sesh), str)
        self.assertTrue(len(str(sesh)) > 5)
        self.assertTrue("SuperSession" in str(sesh))


class TraineeGroupTest(BaseTraineeTest, TrainingTestToolsMixin):
    def setUp(self):
        self.trainingTestToolsSetUp()

    def test_trainees_list(self):
        trainee1 = self.get_trainee()
        trainee2 = self.get_trainee()
        tg = TraineeGroup.objects.create()
        tg.save()
        tg.trainees.add(trainee1, trainee2)

        self.assertIsInstance(tg.trainees_list(), str)
        self.assertTrue(trainee1.get_full_name() in tg.trainees_list())
        self.assertTrue(trainee2.get_full_name() in tg.trainees_list())

    def test_trainees_list_with_links(self):
        trainee1 = self.get_trainee()
        trainee2 = self.get_trainee()
        tg = TraineeGroup.objects.create()
        tg.save()
        tg.trainees.add(trainee1, trainee2)

        self.assertIsInstance(tg.trainees_list(), str)
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
        name = "TEST TG NAME"
        tg = TraineeGroup.objects.create(name=name)
        tg.save()

        self.assertEqual(str(tg), "TG{:0>4d} {}".format(tg.pk, name))
