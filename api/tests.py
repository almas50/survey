from django.test import TestCase
import datetime
from .models import Survey, Question
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse


class SurveyTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        survey = Survey.objects.create(name="test", start_date=datetime.datetime.now().date(),
                                       end_date=datetime.datetime.now().date(), description="test survey")
        survey.save()

    def test_survey_content(self):
        survey = Survey.objects.get(id=1)
        name = survey.name
        descr = survey.description
        self.assertEqual(name, 'test')
        self.assertEqual(descr, 'test survey')


class QuestionTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        survey = Survey.objects.create(name="test", start_date=datetime.datetime.now().date(),
                                       end_date=datetime.datetime.now().date(), description="test survey")
        survey.save()
        question = Question.objects.create(text="ok", type="Text", survey=survey)
        question.save()

    def test_survey_content(self):
        question = Question.objects.get(id=1)
        text = question.text
        type = question.type
        survey = question.survey
        self.assertEqual(text, 'ok')
        self.assertEqual(type, 'Text')
        self.assertEqual(survey.name, "test")


class ViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'test', 'password': 'test'}
        self.response = self.client.post(
            reverse('register'),
            self.user_data,
            format="json")

    def test_can_create_a_user(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
