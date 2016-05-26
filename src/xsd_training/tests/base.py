import testdata

from xSACdb.test_helpers import BaseTest, AsGroupMixin
from xsd_training.models import *


class BaseTraineeTest(BaseTest):
    def setUp(self):
        super(BaseTraineeTest, self).setUp()


class BaseInstructorTest(BaseTraineeTest):
    def setUp(self):
        super(BaseInstructorTest, self).setUp()
        self.mp.set_qualification(Qualification.objects.get(code="OWI"))
        self.mp.save()


class BaseTrainingTest(AsGroupMixin, BaseTest):
    GROUPS = [3]


class TrainingTestToolsMixin(object):
    def setUp(self):
        self.trainingTestToolsSetUp()
        super(TrainingTestToolsMixin, self).setUp()

    def trainingTestToolsSetUp(self):
        self.OD = Qualification.objects.get(code="OD")
        self.SD = Qualification.objects.get(code="SD")
        self.DL = Qualification.objects.get(code="DL")
        self.AD = Qualification.objects.get(code="AD")
        self.FC = Qualification.objects.get(code="FC")

        self.PERSONAL_QUALS = [self.OD, self.SD, self.DL, self.AD, self.FC]

        self.ADI = Qualification.objects.get(code="ADI")
        self.PI = Qualification.objects.get(code="PI")
        self.THI = Qualification.objects.get(code="THI")
        self.AOWI = Qualification.objects.get(code="AOWI")
        self.OWI = Qualification.objects.get(code="OWI")
        self.AI = Qualification.objects.get(code="AI")
        self.NI = Qualification.objects.get(code="NI")

        self.INSTRUCTOR_QUALS = [self.ADI, self.PI, self.THI, self.AOWI, self.OWI,
                                 self.AI, self.NI]

        self.OO1 = Lesson.objects.get(code="OO1")
        self.OO2 = Lesson.objects.get(code="OO2")
        self.SO1 = Lesson.objects.get(code="SO1")

        self.BOAT_HANDLING = SDC.objects.get(title="Boat Handling")
        self.WRECK_APPRECIATION = SDC.objects.get(title="Wreck Appreciation")

    def get_trainee(self, training_for=None):
        if not training_for: training_for = self.OD
        user = self.create_a_user()
        user.training_for = [training_for]
        user.save()
        return user.get_profile()

    def get_instructor(self, qualification=None):
        if not qualification: qualification = self.OWI
        user = self.create_a_user()
        mp = user.get_profile()
        mp.set_qualification(self.OWI)
        mp.save()
        return user.get_profile()

    def create_basic_pl(self, trainee=None):
        if not trainee: trainee = self.get_trainee()
        pl = PerformedLesson.objects.create(
            trainee=trainee
        )
        pl.save()
        return pl

    def create_pl(self, trainee=None, instructor=None):
        if not trainee: trainee = self.get_trainee()
        if not instructor: trainee = self.get_instructor()
        pl = PerformedLesson.objects.create(
            trainee=trainee,
            instructor=instructor,
        )
        pl.save()
        return pl

    def create_session(self, site):
        sesh = Session.objects.create(
            name=testdata.get_str(str_size=64),
            when=testdata.get_future_datetime(),
            where=site,
        )
        sesh.save()
        return sesh
