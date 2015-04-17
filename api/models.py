from django.db import models

# Create your models here.

#Model for Director
class Director(models.Model):
  name = models.CharField(max_length = 200)

  def __str__(self):
    return self.name

#Model for Genre
class Genre(models.Model):
  name = models.CharField(max_length = 50)

#Model for Movie
class Movie(models.Model):
  name = models.CharField(max_length = 100)
  imdb_score = models.FloatField()
  popularity = models.FloatField()
  director = models.ForeignKey(Director)
  genres = models.ManyToManyField(Genre)
