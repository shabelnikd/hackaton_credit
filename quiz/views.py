from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question
from .serializers import QuestionSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuizResultView(APIView):
    def post(self, request, *args, **kwargs):
        answers = request.data.get('answers', [])
        score = 0

        for answer in answers:
            question_id = answer.get('question_id')
            selected_answer = answer.get('answer_id')

            try:
                question = Question.objects.get(id=question_id)
                correct_answer = question.correct_answer
                if correct_answer == selected_answer:
                    score += 1
            except Question.DoesNotExist:
                continue

        return Response({'score': score, 'total': len(answers)}, status=status.HTTP_200_OK)
