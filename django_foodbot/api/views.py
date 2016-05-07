from datetime import datetime, timedelta

from django.http import Http404

from rest_framework import filters, status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response

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

    def check_item_exist(self, item_id):
        try:
            return Menu.objects.get(id=item_id)
        except Menu.DoesNotExist:
            raise Http404

    def post(self, request, id, format=None):
        menu = self.check_item_exist(id)

        ratings_dict = request.data
        ratings_dict.update({unicode('menu'): unicode(id)})

        rating_serializer = RatingSerializer(data=ratings_dict)

        if rating_serializer.is_valid():
            import pdb; pdb.set_trace()
            rating_serializer.save()
            content = {'status': 'Success'}
            return Response(content, status=status.HTTP_201_CREATED)

        return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
