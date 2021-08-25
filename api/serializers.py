from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Survey, Question, Answer, Response, Option
from rest_framework.exceptions import ValidationError


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('text',)


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ('text', 'type', 'survey', 'options')

    def create(self, validated_data):
        options = validated_data.pop('options')
        question = Question.objects.create(**validated_data)
        for option in options:
            Option.objects.create(text=option['text'], question=question)
        return question


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'

    def update(self, instance, validated_data):
        validated_data.pop('start_date', None)
        return super().update(instance, validated_data)


class RegisterUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password')


class ResponseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('text', 'question')


class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Response
        fields = ('survey', 'created', 'answers')

    def validate_answers(self, answers):
        for answer in answers:
            question_type = answer['question'].type
            if question_type == 'ONEANSWER' or question_type == 'MULTIANSWER':
                if not answer['text'].isdigit():
                    raise ValidationError('You should choose answer from options')
        return answers

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        response = Response.objects.create(survey=validated_data.pop('survey'), user=self.context['request'].user)
        for answer in answers:
            Answer.objects.create(response=response, user=self.context['request'].user, text=answer['text'],
                                  question=answer['question'])
        return response
