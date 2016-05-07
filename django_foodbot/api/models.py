from django.db import models


class Menu(models.Model):

    day = models.CharField(max_length=10, blank=False, null=False)
    food = models.TextField()
    meal = models.CharField(max_length=10, blank=False, null=False)
    option = models.IntegerField(null=False)
    week = models.IntegerField(null=False)

    class Meta:
        ordering = ('-week',)
        db_table = 'menu_table'

    def __unicode__(self):
        return u'%s %s %s' % (self.day, self.week, self.meal)


class Rating(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=20, blank=False, null=False)
    menu = models.ForeignKey(Menu, related_name='rating')
    rate = models.IntegerField(blank=False, null=False)
    comment = models.TextField(default='no comment')

    class Meta:
        ordering = ('-created_at',)
        db_table = 'rating'

    def __unicode__(self):
        return u'%s' % (self.created_at)
