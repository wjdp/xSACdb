import random

class MemberProfileFakeDataMixin(object):
    def fake(self, fake):
        self.date_of_birth = fake.date_time_between(start_date="-90y", end_date="-12y", tzinfo=None).date()
        self.gender = random.choice(('m', 'f'))
        self.address = fake.address()
        self.postcode = fake.postcode()
        self.home_phone = fake.phone_number()
        self.mobile_phone = fake.phone_number()
        self.next_of_kin_name = fake.name()
        self.next_of_kin_relation = random.choice(('Mother', 'Father', 'Mum', 'Dad', 'Partner', 'Wife',
                                                   'Husband', 'Dog', 'Cat', 'Fish', 'Tortoise'))
        self.next_of_kin_phone = fake.phone_number()

        if fake.boolean(chance_of_getting_true=50):
            self.student_id = random.randrange(1234567, 9999999)

        self.veggie = fake.boolean(chance_of_getting_true=10)
        if fake.boolean(chance_of_getting_true=50):
            self.alergies = fake.paragraph()

        # Most people are current, 15% are out of date
        if fake.boolean(chance_of_getting_true=85):
            self.club_expiry = fake.date_time_between(start_date="-30d", end_date="+2y", tzinfo=None).date()
            self.bsac_expiry = fake.date_time_between(start_date="-30d", end_date="+2y", tzinfo=None).date()
            self.medical_form_expiry = fake.date_time_between(start_date="-30d", end_date="+2y", tzinfo=None).date()
        else:
            if fake.boolean(chance_of_getting_true=60):
                self.club_expiry = fake.date_time_between(start_date="-6y", end_date="+1y", tzinfo=None).date()
            if fake.boolean(chance_of_getting_true=60):
                self.bsac_expiry = fake.date_time_between(start_date="-6y", end_date="+1y", tzinfo=None).date()
            if fake.boolean(chance_of_getting_true=60):
                self.medical_form_expiry = fake.date_time_between(start_date="-6y", end_date="+3y", tzinfo=None).date()
