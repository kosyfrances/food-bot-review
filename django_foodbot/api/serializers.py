from rest_framework import serializers
from api.models import Menu, Rating


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model=Rating
        fields=('id', 'date', 'user_id', 'menu', 'comment')




class MenuSerializer(serializers.ModelSerializer):

    rating= RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ('id','day','rating','food', 'meal', 'option', 'week') 
        

