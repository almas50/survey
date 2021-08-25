from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .permisisions import IsAdminOrReadOnly
from .models import Survey, Question, Response
from .serializers import SurveySerializer, QuestionSerializer, RegisterUserSerializer, ResponseSerializer
from rest_framework.generics import CreateAPIView, ListAPIView


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAdminOrReadOnly]


class ListSurvey(ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RegisterUser(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer


class CreateResponse(CreateAPIView):
    serializer_class = ResponseSerializer
    queryset = Response.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super(CreateResponse, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class ListResponses(ListAPIView):
    serializer_class = ResponseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Response.objects.filter(user=user)





