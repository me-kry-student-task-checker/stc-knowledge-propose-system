from django.test import TestCase
from rest_framework.test import APITestCase
from calculator_app.models import Calculations


class CalculationsTest(TestCase):

    def setUp(self):
        Calculations.objects.create(numbera=1, numberb=2, operation="add", result=3)

    def test_fields(self):
        calculation = Calculations.objects.get(result=3)
        self.assertEqual(calculation.result, 3)
