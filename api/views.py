from api.models import Movie, Director, Genre
from api.serializers import MovieSerializer, DirectorSerializer, GenreSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from api.permissions import IsAuthenticatedAndIsAdminOrReadOnly


class MovieList(APIView):
  """
  List all movies or create a new movie
  """
  permission_classes = (IsAuthenticatedAndIsAdminOrReadOnly, )  #Checking for admin login
  def get(self, request, format=None):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

  def post(self, request, format=None):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieDetail(APIView):
  """
  Retrive, update or delete a movie instance
  """
  permission_classes = (IsAuthenticatedAndIsAdminOrReadOnly, )   #Checking for admin login
  def get_object(self, pk):
    try:
      return Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
      raise Http404

  def get(self, request, pk, format=None):
    movie = self.get_object(pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

  def put(self, request, pk, format=None):
    movie = self.get_object(pk)
    serializer = MovieSerializer(movie, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    movie = self.get_object(pk)
    movie.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class MovieSearch(APIView):
  """
  Search for movies
  """
  def post(self, request, format=None):
    search_term = request.data.pop('query')

    movie_list = Movie.objects.filter(name__icontains=search_term) #filtering search request on movie name
    director_list = Movie.objects.filter(director__name__icontains=search_term) #filtering search request on director name
    genre_list = Movie.objects.filter(genres__name__icontains=search_term) #filtering search request on genre name
    final_list = movie_list | director_list | genre_list #appending all the results
    final_list = final_list.distinct();
    
    serializer = MovieSerializer(final_list, many=True)
    return Response(serializer.data)