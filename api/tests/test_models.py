from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from api.models import Entity, Type


class EntityModelTest(TestCase):

    def setUp(self):
        self.type = Type.objects.create(type_id=4, description='State')
        self.entity = Entity.objects.create(
            county_code = '00',
            district_code = '00000',
            school_code = '0000000',
            test_year = '2016',
            entity_type = self.type,
            county_name = 'State of California'
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.entity),
            '00-00000-0000000 State of California'
        )

    def test_verbose_name_plural(self):
        self.assertEqual(str(Entity._meta.verbose_name_plural), 'entities')

    def test_county_code_max_length(self):
        self.entity.county_code = '0' * 3
        with self.assertRaises(ValidationError):
            self.entity.save()
            self.entity.full_clean()

    def test_district_code_max_length(self):
        self.entity.district_code = '0' * 6
        with self.assertRaises(ValidationError):
            self.entity.save()
            self.entity.full_clean()

    def test_school_code_max_length(self):
        self.entity.school_code = '0' * 8
        with self.assertRaises(ValidationError):
            self.entity.save()
            self.entity.full_clean()

    def test_county_name_max_length(self):
        self.entity.county_name = 'a' * 201
        with self.assertRaises(ValidationError):
            self.entity.save()
            self.entity.full_clean()

    def test_district_name_max_length(self):
        self.entity.district_name = 'a' * 1001
        with self.assertRaises(ValidationError):
            self.entity.save()
            self.entity.full_clean()

    def test_school_name_max_length(self):
        self.entity.school_name = 'a' * 1001
        with self.assertRaises(ValidationError):
            self.entity.save()
            self.entity.full_clean()

    def test_zipcode_max_length(self):
        self.entity.zipcode = '1' * 13
        with self.assertRaises(ValidationError):
            self.entity.save()
            self.entity.full_clean()

    def test_district_name_can_be_blank(self):
        self.entity.district_name = ''
        try:
            self.entity.save()
            self.entity.full_clean()
        except Error:
            print('Blank district name should not throw error.')

    def test_school_name_can_be_blank(self):
        self.entity.school_name = ''
        try:
            self.entity.save()
            self.entity.full_clean()
        except Error:
            print('Blank school name should not throw error.')

    def test_zipcode_can_be_blank(self):
        self.entity.zipcode = ''
        try:
            self.entity.save()
            self.entity.full_clean()
        except Error:
            print('Blank zipcode should not throw error.')


class TypeModelTest(TestCase):

    def setUp(self):
        self.entity_type = Type.objects.create(
            type_id=1,
            description='Test Entity Type'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.entity_type), 'Test Entity Type')

    def test_type_id_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            duplicate = Type.objects.create(
                type_id=1,
                description='Duplicate Entity Type'
            )

    def test_description_max_length(self):
        self.entity_type.description = 'a' * 31
        with self.assertRaises(ValidationError):
            self.entity_type.save()
            self.entity_type.full_clean()