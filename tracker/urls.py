from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicViewSet, QuestionViewSet, UserProgressViewSet
from .views import generate_ai_question, analyze_ai_answer, save_progress, get_progress
from .views import mock_interview, hot_topics, generate_aptitude_question

router = DefaultRouter()
router.register(r'topics', TopicViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'progress', UserProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ai/generate/', generate_ai_question),
    path('ai/analyze/', analyze_ai_answer),
    path('save-progress/', save_progress),
    path('get-progress/', get_progress),
    path('mock-interview/', mock_interview),
    path('hot-topics/', hot_topics),
    path('aptitude/', generate_aptitude_question),
]
