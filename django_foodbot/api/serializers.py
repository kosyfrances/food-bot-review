from rest_framework import serializers

from api.models import Menu, Rating


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ('id', 'day', 'food', 'meal', 'option', 'week')


class RatingSerializer(serializers.ModelSerializer):

    menu = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'created_at', 'user_id', 'rate', 'comment', 'rating')
