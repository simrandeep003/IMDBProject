from django.forms import widgets
from rest_framework import serializers
from api.models import Movie, Director, Genre

class DirectorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Director
    fields = ('id', 'name')
    read_only_fields = ('id',)

class GenreSerializer(serializers.ModelSerializer):
  class Meta:
    model = Genre
    fields = ('id', 'name')
    read_only_fields = ('id',)


class MovieSerializer(serializers.ModelSerializer):
  director = DirectorSerializer()
  genres = GenreSerializer(many=True)
  class Meta:
    model = Movie
    fields = ('id', 'name', 'imdb_score', 'popularity', 'director', 'genres')
    read_only_fields = ('id',)

  def create(self, validated_data):
    director_data = validated_data.pop('director')
    genres_data = validated_data.pop('genres')
    try:
      director_exists = Director.objects.get(name=director_data['name'])
      validated_data['director_id'] = director_exists.pk
    except Director.DoesNotExist:
      d = Director.objects.create(name=director_data['name'])
      validated_data['director_id'] = d.pk
    movie = Movie.objects.create(**validated_data)
    for data in genres_data:
      try:
        g = Genre.objects.get(name=data['name'])
      except Genre.DoesNotExist:
        g = Genre.objects.create(name=data['name'])
      movie.genres.add(g)
    return movie



  def update(self, instance, validated_data):
    instance.name = validated_data.get('name','instance.name')
    instance.imdb_score = validated_data.get('imdb_score','instance.imdb_score')
    instance.popularity = validated_data.get('popularity','instance.popularity')
    
    director_data = validated_data.pop('director')
    try:
      director_exists = Director.objects.get(name=director_data['name'])
      validated_data['director_id'] = director_exists.pk
    except Director.DoesNotExist:
      d = Director.objects.create(name=director_data['name'])
      validated_data['director_id'] = d.pk

    instance.director_id = validated_data.get('director_id','instance.director_id')
    
    genres_data = validated_data.pop('genres')

    movie = Movie.objects.get(pk=instance.pk)
    movie.genres.clear()

    for data in genres_data:
      try:
        g = Genre.objects.get(name=data['name'])
      except Genre.DoesNotExist:
        g = Genre.objects.create(name=data['name'])
      instance.genres.add(g)
    
    instance.save()
    return instance
    
