from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Survey,Question, Answers, Response, Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields =('id', 'value')


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


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


class AnswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = ('text',)


class ResponseSerializer(serializers.ModelSerializer):
    answers = AnswersSerializer(many=True)

    class Meta:
        model = Response
        fields = ('survey', 'created', 'answers')

    # todo write validate function
    def validate_answers(self, answers):
        pass

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        response = Response.objects.create(**validated_data, user=self.context['request'].user)
        Answers.objects.create(response=response, user=self.context['request'].user, text=answers)
        return response


