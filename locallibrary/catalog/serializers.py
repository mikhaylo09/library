from django.contrib.auth.models import User
from .models import Author, Book, Genre, Language, BookInstance, Review
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = serializers.CharField(max_length=255)
    genre = serializers.StringRelatedField(many=True)
    language = serializers.CharField(max_length=255)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'summary', 'isbn', 'genre', 'language', 'reviews', 'rating']

class BookDestroyedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'destroy', 'user_destroy', 'date_destroy']

class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = '__all__'

