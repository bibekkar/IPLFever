from django.db import models

# Create your models here.
class Usertable(models.Model):
    user_id = models.CharField(max_length=10)
    pwd = models.CharField(max_length=20)

    def __str__(self):
        return self.user_id +" "+ self.pwd


class fixtures(models.Model):

    team1 = models.CharField(max_length=3)
    team2 = models.CharField(max_length=3)
    date = models.DateField()
    time = models.CharField(max_length=15)
    venue = models.CharField(max_length=50)
    result = models.CharField(max_length=3)







class betting(models.Model):
    match_id = models.IntegerField()
    user_id = models.CharField(max_length=10)
    team = models.CharField(max_length=3)
    amount = models.FloatField()




