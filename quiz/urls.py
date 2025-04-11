from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, QuizResultView


router = DefaultRouter()
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('result/', QuizResultView.as_view(), name='quiz-result'),
]
