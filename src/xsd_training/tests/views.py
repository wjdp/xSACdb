import uuid

from xSACdb.test_helpers import ViewTestMixin
from xsd_sites.tests import SiteTestToolsMixin
from xsd_training.views import *
from .base import *


class TrainingDashboardViewTest(TrainingTestToolsMixin, ViewTestMixin, BaseTraineeTest):
    url_name = 'xsd_training:training-overview'
    template_name = 'overview.html'

    def test_content(self):
        r = self.response

        self.assertContains(r, 'Ocean Diver')
        self.assertContains(r, 'Sports Diver')
        self.assertContains(r, 'Dive Leader')
        self.assertContains(r, 'Advanced Diver')
        self.assertContains(r, 'First Class Diver')

    def test_content_with_tf(self):
        # Set training_for so list appears
        self.mp.training_for = self.OD
        self.mp.save()

        r = self.get_response()

        self.assertContains(r, 'Ocean Diver')
        self.assertContains(r, 'Sports Diver')
        self.assertContains(r, 'Dive Leader')
        self.assertContains(r, 'Advanced Diver')
        self.assertContains(r, 'First Class Diver')


class TrainingLessonsViewTest(TrainingTestToolsMixin, ViewTestMixin, BaseTraineeTest):
    url_name = 'xsd_training:training-lessons'
    template_name = 'lessons.html'

    @classmethod
    def setUp_test(cls):
        cls.mp.training_for = cls.OD
        cls.mp.save()

    def test_content(self):
        r = self.response
        self.assertContains(r, 'Ocean Diver')
        self.assertContains(r, 'OT1 - Adapting to the underwater world')

        # def test_200_no_tf(self):
        #     self.mp.training_for = None
        #     self.mp.save()
        #     c = self.get_client()
        #     r = c.get(self.URL)
        #     self.assertEqual(r.status_code, 200) # TODO failing
        #
        #
        # def test_content_no_tf(self):
        #     self.mp.training_for = None
        #     self.mp.save()
        #     c = self.get_client()
        #     r = c.get(self.URL)
        #     # TODO add content check, need to write content


# TODO lesson detail

class TrainingFeedbackViewTest(ViewTestMixin, BaseTraineeTest):
    url_name = 'xsd_training:all-feedback'
    template_name = 'all_feedback.html'

    # TODO add some feedback, check


# TODO pl-mouseover-api

# TODO session/new
# TODO session/list
# TODO sessiondetail
# TODO session complete
# TODO session delete

# TODO pool sheet create

class PoolSheetViewTest(BaseTrainingTest):
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

    def test_form(self):
        c = self.get_client()
        url = reverse('xsd_training:PoolSheet')
        r = c.get(url)
        self.assertEqual(r.status_code, 200)

    def test_dumb_ps_pool(self):
        self.generic_ps(self.url_ow)

    def test_dumb_ps_ow(self):
        self.generic_ps(self.url_ow)

    def test_dumb_ps_theory(self):
        self.generic_ps(self.url_theory)


# TODO retro lessons

# TODO qualification award

class InstructorUpcomingViewTest(ViewTestMixin, TrainingTestToolsMixin, SiteTestToolsMixin, BaseInstructorTest):
    url_name = 'xsd_training:InstructorUpcoming'
    template_name = 'instructor_upcoming.html'

    def create_instructor_session(self, when, trainee=None, instructor=None):
        if trainee is None:
            trainee = self.get_trainee()
        if instructor is None:
            instructor = self.get_instructor()

        sesh = Session.objects.create(
            name=self.fake.name(),
            when=when,
            where=self.create_site(),
            notes=uuid.uuid4(),  # allow us to search for this easily in responses
        )
        sesh.save()
        pl = self.create_pl(trainee, instructor)
        pl.session = sesh
        pl.save()
        return sesh

    def test_content(self):
        r = self.response
        # check empty
        self.assertContains(r, 'You do not have any upcoming sessions')

        # create some sessions to work with
        past_sesh = self.create_instructor_session(
            self.get_past_datetime() - Session.LESSON_HISTORY,  # pad to make sure its well outside our timeframe
            instructor=self.mp
        )
        future_sesh = self.create_instructor_session(self.get_future_datetime(), instructor=self.mp)
        last_sesh = self.create_instructor_session(datetime.datetime.now() - (Session.LESSON_HISTORY / 2),
                                                   instructor=self.mp)
        todays_sesh = self.create_instructor_session(datetime.datetime.now(), instructor=self.mp)

        r = self.get_response()
        self.assertNotContains(r, past_sesh.notes)
        self.assertContains(r, future_sesh.notes)
        self.assertContains(r, last_sesh.notes)
        self.assertContains(r, todays_sesh.notes)


# TODO trainee notes search
# TODO trainee notes detail
# TODO trainee set field

class SDCListViewTest(ViewTestMixin, BaseTraineeTest):
    url_name = 'xsd_training:SDCList'
    view = SDCList

    def test_content(self):
        r = self.response
        # Check a header and two SDCs
        self.assertContains(r, 'Club Diving')
        self.assertContains(r, 'Compressor Operation')
        self.assertContains(r, 'Advanced Lifesaver Award')


# TODO SDC register interest

class PSDCPlanViewTest(TrainingTestToolsMixin, ViewTestMixin, BaseTrainingTest):
    url_name = 'xsd_training:PerformedSDCCreate'
    view = PerformedSDCCreate

    # TODO actually create a PSDC


class PSDCListViewTest(ViewTestMixin, BaseTraineeTest):
    url_name = 'xsd_training:PerformedSDCList'
    view = PerformedSDCList

    def setUp_single_SDC(self):
        sdc = SDC.objects.all()[0]
        psdc = PerformedSDC.objects.create(
            sdc=sdc,  # Lazily get the first SDC from BSAC data
            datetime=self.get_random_date(),
        )
        psdc.save()
        return psdc

    def test_content(self):
        r = self.response
        # There should be no PSDCs
        self.assertContains(r, 'No SDCs have been planned')

    def test_content_with_psdc(self):
        psdc = self.setUp_single_SDC()
        r = self.get_response()
        self.assertContains(r, psdc.sdc.title)


# TODO PSDC detail
# TODO PSDC edit
# TODO PSDC complete
# TODO PSDC delete

# TODO SDC award

# TODO group list
# TODO group create
# TODO group detail
# TODO group complete

class TraineeGroupList(ViewTestMixin, BaseTrainingTest):
    url_name = 'xsd_training:TraineeGroupList'
    view = TraineeGroupList

    def test_content(self):
        TG_NAME = "TestTraineeGroup1"
        tg = TraineeGroup.objects.create(name=TG_NAME)
        r = self.get_response()
        self.assertContains(r, TG_NAME)


class TraineeGroupCreate(ViewTestMixin, BaseTrainingTest):
    url_name = 'xsd_training:TraineeGroupCreate'
    view = TraineeGroupCreate

    def test_create(self):
        # TODO export this to a FormIntegrationTestMixin
        TG_NAME = self.fake.name()
        c = self.get_client()
        r = c.post(self.get_url(), {'name': TG_NAME})
        tg = TraineeGroup.objects.filter(name=TG_NAME)
        self.assertEqual(r.status_code, 302)  # 200) # redirects to list
        self.assertEqual(len(tg), 1)

    def test_create_tg_invalid(self):
        # Create group using HTTP and check it doesn't
        c = self.get_client()
        r = c.post(self.get_url())
        tgs = TraineeGroup.objects.all()
        self.assertEqual(len(tgs), 0)


class TraineeGroupUpdate(ViewTestMixin, BaseTrainingTest):
    url_name = 'xsd_training:TraineeGroupUpdate'
    view = TraineeGroupUpdate

    @classmethod
    def setUp_test(cls):
        cls.TG_NAME = "TESTGROUP"
        tg = TraineeGroup.objects.create(name=cls.TG_NAME)
        cls.url_kwargs = {'pk': tg.pk}

    def test_content(self):
        r = self.response
        self.assertContains(r, self.TG_NAME)


class TraineeGroupDelete(ViewTestMixin, BaseTrainingTest):
    url_name = 'xsd_training:TraineeGroupDelete'
    view = TraineeGroupDelete

    @classmethod
    def setUp_test(cls):
        cls.TG_NAME = cls.fake.name()
        tg = TraineeGroup.objects.create(name=cls.TG_NAME)
        cls.url_kwargs = {'pk': tg.pk}

    def test_delete(self):
        # TODO export this as DeleteViewTestMixin
        qs = TraineeGroup.objects.filter(name=self.TG_NAME)
        c = self.get_client()
        self.assertEqual(qs.count(), 1)
        c.post(self.get_url())
        self.assertEqual(qs.count(), 0)

# TODO group progress
