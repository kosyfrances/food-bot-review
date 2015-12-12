from rest_framework import serializers

from api.models import Menu, Rating


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ('id', 'day', 'food', 'meal', 'option', 'week')


class RatingSerializer(serializers.ModelSerializer):

    menu = MenuSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'date', 'user_id', 'menu', 'rate', 'comment')
