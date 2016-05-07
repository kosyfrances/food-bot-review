from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView

from api.models import Menu, Rating
from api.serializers import RatingSerializer, MenuSerializer
from api.setpage import LimitOffsetpage


class MenuList(ListAPIView):

    """
    List all the Menu items.
    """
    model = Menu
    serializer_class = MenuSerializer
    pagination_class = LimitOffsetpage
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')

    def get_queryset(self):
        """
        This view should return a list of all the Menu
        for the currently authenticated user.
        """
        queryset = Menu.objects.all()

        return queryset


class RatingList(ListAPIView):
    """
    List all ratings and comments
    """
    model = Rating
    serializer_class = RatingSerializer
    pagination_class = LimitOffsetpage
    filter_backends = (filters.SearchFilter,)
    search_fields = ('created_at')

    def get_queryset(self):
        """
        This view should return a list of all the Ratings and Comments
        for the currently authenticated user.
        """
        queryset = Rating.objects.all()

        return queryset


class WeeklyRatings(ListAPIView):
    """
    List all ratings and comments for the week
    """
    model = Rating
    serializer_class = RatingSerializer
    pagination_class = LimitOffsetpage
    filter_backends = (filters.SearchFilter,)
    search_fields = ('created_at')

    def get_queryset(self):

        enddate = datetime.today()
        startdate = enddate + timedelta(days=-8)
        queryset = Rating.objects.filter(created_at__range=[startdate, enddate])

        return queryset


class PostRatings(CreateAPIView):
    """Post ratings and comments."""

    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        menu = get_object_or_404(Menu, pk=self.kwargs.get('id'))
        serializer.save(menu=menu)
