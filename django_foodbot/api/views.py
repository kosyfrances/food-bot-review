from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from api.models import MenuTable, Rating
from api.serializers import RatingSerializer, MenuTableSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import Http404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from .setpage import LimitOffsetpage

from rest_framework import filters
from rest_framework.generics import GenericAPIView, ListAPIView
# Create your views here.
