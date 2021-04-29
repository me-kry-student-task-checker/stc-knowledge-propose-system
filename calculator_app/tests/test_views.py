from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.utils import json

from calculator_app.models import Calculations
from calculator_app.serializers import CalculationSerializer

client = APIClient()


class GetCalculationsTest(APITestCase):

    def setUp(self):
        Calculations.objects.create(numbera=1, numberb=2, operation="add", result=3)
        Calculations.objects.create(numbera=2, numberb=2, operation="multiple", result=4)

    def test_get_all_calculations(self):
        response = client.get("/logs/")
        calculations = Calculations.objects.all()
        serializer = CalculationSerializer(calculations, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CalculateTest(APITestCase):

    def setUp(self):
        self.valid_calculation = {
            "numberA": 4,
            "numberB": 2,
            "operation": "divide"
        }
        self.invalid_calculation = {
            "numberA": 3,
            "numberB": 2,
            "operation": "dive"
        }

    def test_valid_calculate(self):
        response = client.post("/calc/", data=json.dumps(self.valid_calculation), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_calculate(self):
        response = client.post("/calc/", data=json.dumps(self.invalid_calculation), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

