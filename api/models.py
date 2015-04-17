from django.db import models

# Create your models here.
class Director(models.Model):
  name = models.CharField(max_length = 200)

  def __str__(self):
    return self.name

class Genre(models.Model):
  name = models.CharField(max_length = 50)

class Movie(models.Model):
  name = models.CharField(max_length = 100)
  imdb_score = models.FloatField()
  popularity = models.FloatField()
  director = models.ForeignKey(Director)
  genres = models.ManyToManyField(Genre)
