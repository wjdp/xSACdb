from xSACdb.roles.groups import GROUP_TRAINING
from xSACdb.test_helpers import BaseTest, AsGroupMixin
from xsd_training.models import *


class BaseTraineeTest(BaseTest):
    pass


class BaseInstructorTest(BaseTraineeTest):
    @classmethod
    def setUp_base(cls):
        cls.mp.set_qualification(Qualification.objects.get(code="OWI"))
        cls.mp.save()
        super(BaseInstructorTest, cls).setUp_base()


class BaseTrainingTest(AsGroupMixin, BaseTest):
    GROUPS = [GROUP_TRAINING]


class TrainingTestToolsMixin:
    @classmethod
    def setUp_base(cls):
        cls.trainingTestToolsSetUp()
        super(TrainingTestToolsMixin, cls).setUp_base()

    @classmethod
    def trainingTestToolsSetUp(cls):
        cls.OD = Qualification.objects.get(code="OD")
        cls.ODL = Qualification.objects.get(code="ODL")
        cls.SD = Qualification.objects.get(code="SD")
        cls.DL = Qualification.objects.get(code="DL")
        cls.AD = Qualification.objects.get(code="AD")
        cls.FC = Qualification.objects.get(code="FC")

        cls.PERSONAL_QUALS = [cls.OD, cls.SD, cls.DL, cls.AD, cls.FC]

        cls.ADI = Qualification.objects.get(code="ADI")
        cls.PI = Qualification.objects.get(code="PI")
        cls.TI = Qualification.objects.get(code="TI")
        cls.AOWI = Qualification.objects.get(code="AOWI")
        cls.OWI = Qualification.objects.get(code="OWI")
        cls.AI = Qualification.objects.get(code="AI")
        cls.NI = Qualification.objects.get(code="NI")

        cls.INSTRUCTOR_QUALS = [cls.ADI, cls.TI, cls.PI, cls.AOWI, cls.OWI,
                                cls.AI, cls.NI]
        cls.ACTIVE_QUALS = cls.PERSONAL_QUALS + cls.INSTRUCTOR_QUALS

        cls.OO1 = Lesson.objects.get(code="OO1", qualification=cls.OD)
        cls.OO2 = Lesson.objects.get(code="OO2", qualification=cls.OD)
        cls.SO1 = Lesson.objects.get(code="SO1")

        cls.BOAT_HANDLING = SDC.objects.get(title="Boat Handling")
        cls.WRECK_APPRECIATION = SDC.objects.get(title="Wreck Appreciation")

    def get_trainee(self, training_for=None):
        if not training_for: training_for = self.OD
        user = self.create_a_user()
        user.training_for = [training_for]
        user.save()
        return user.get_profile()

    def get_instructor(self, qualification=None):
        if not qualification: qualification = self.OWI
        user = self.create_a_user(verified=True)
        mp = user.get_profile()
        mp.set_qualification(qualification)
        mp.save()
        return user.get_profile()

    def get_training_officer(self):
        user = self.create_a_user(verified=True)
        user.groups.add(GROUP_TRAINING)
        user.save()
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
        if not instructor: instructor = self.get_instructor()
        pl = PerformedLesson.objects.create(
            trainee=trainee,
            instructor=instructor,
        )
        pl.save()
        return pl

    def create_session(self, site):
        sesh = Session.objects.create(
            name=self.fake.name(),
            when=self.get_future_datetime(),
            where=site,
        )
        sesh.save()
        return sesh
