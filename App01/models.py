# models.py
from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

class BusanDistrict(models.Model):
    district_name = models.CharField(max_length=100)
    population = models.IntegerField()
    area = models.FloatField()
    major_facility = models.CharField(max_length=200)

    def __str__(self):
        return self.district_name  # district_name을 반환하도록 수정
