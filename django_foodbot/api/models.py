from django.db import models

# Create your models here.

class Menu(models.Model):

    day=models.CharField(max_length=10, blank=False, null=False)
    food=models.CharField(max_length=60, blank=False, null=False)
    meal=models.CharField(max_length=10, blank=False, null=False)
    option=models.IntegerField(null=False)
    week=models.IntegerField(null=False)

    class Meta:
        ordering = ('-week',)
        db_table = 'menu_table'
        

class Rating(models.Model):

    date=models.DateTimeField(auto_now_add = True)
    user_id=models.CharField(max_length=20)
    menu=models.ForeignKey(Menu, related_name='rating')
    rate=models.IntegerField(blank=False, null=False)
    comment=models.TextField(default='no comment', )

    class Meta:
        ordering = ('-date',)
        db_table = 'rating'
