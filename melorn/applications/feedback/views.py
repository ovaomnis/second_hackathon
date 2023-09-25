from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from applications.feedback.models import Comment
from applications.feedback.serializers import CommentSerializer
from applications.feedback.permissions import IsAuthenticatedOrIsOwnerOrAdmin


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes =[IsAuthenticatedOrIsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
