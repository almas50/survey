from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import SurveyViewSet, QuestionViewSet, RegisterUser, ListResponses, CreateResponse

router = SimpleRouter()
router.register('questions', QuestionViewSet, basename='questions')
router.register('survey', SurveyViewSet, basename='surveys')
urlpatterns = router.urls
urlpatterns += [
    path('pass_survey', CreateResponse.as_view()),
    path('register_user', RegisterUser.as_view(), name="register"),
    path('responses', ListResponses.as_view())
]
