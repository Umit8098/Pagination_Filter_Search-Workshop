from rest_framework.viewsets import ModelViewSet

from .serializers import Todo, TodoSerializer
from .pagination import (
    CustomPageNumberPagination,
    CustomLimitOffsetPagination,
    CustomCursorPagination,
)

from django_filters.rest_framework import DjangoFilterBackend



class TodoView(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    # pagination_class = CustomPageNumberPagination
    # pagination_class = CustomLimitOffsetPagination
    # pagination_class = CustomCursorPagination
    
    # filterset_fields = ['title']

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'description']