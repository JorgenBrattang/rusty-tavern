from django.db import models


class Reservation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    table_for = models.PositiveIntegerField(default=1)
    Date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.name
