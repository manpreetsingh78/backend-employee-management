from django.shortcuts import render
from django.db.models import Sum
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.pagination import PageNumberPagination

from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    #--------FILTERS---------
    filter_backends = [SearchFilter]
    search_fields = ['full_name','department']