from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException
from quizzes.models import Quiz, Question
from .permissions import IsOwner
from .pagination import QuizListPagination
from . import serializers


class QuizListMixin(object):
    serializer_class = serializers.QuizListSerializer
    pagination_class = QuizListPagination
    filterset_fields = ('title', 'category__name', 'section__name',)
    filterset_fields = {
        'title': ['istartswith'],
        'category__name': ['exact'],
        'section__name': ['exact'],
    }

    def list(self, request, *args, **kwargs):
        qs = self.filter_queryset(
            self.get_queryset())

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)

        return Response(serializer.data)


class QuestionMixin(object):
    permission_classes = (IsOwner,)
    serializer_class = serializers.QuestionSerializer

    def get_queryset(self, *args, **kwargs):
        author_slug = self.kwargs.get('author_slug')
        quiz_slug = self.kwargs.get('quiz_slug')

        try:
            quiz = Quiz.objects.get(author__slug=author_slug, slug=quiz_slug)
        except ObjectDoesNotExist:
            raise APIException(
                _('The quiz you are looking for does not exist'))

        return Question.objects.filter(quiz=quiz)
