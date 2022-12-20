from django.db import models


class Reservation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    number_of_persons = models.PositiveIntegerField(default=1)
    Date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.name
