from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from api.models import Menu, Rating
from api.serializers import RatingSerializer, MenuSerializer
from rest_framework.response import Response
#from rest_framework.authtoken.models import Token
from django.http import Http404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .setpage import LimitOffsetpage

from rest_framework import filters
from rest_framework.generics import GenericAPIView, ListAPIView
# Create your views here.


class MenuList(ListAPIView):

    """
    List all the Menu items.
    """
    model = Menu
    serializer_class = MenuSerializer
    pagination_class = LimitOffsetpage
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('name')

    def get_queryset(self):
        """
        This view should return a list of all the Menu
        for the currently authenticated user.
        """
        queryset = Menu.objects.all()

        return queryset

