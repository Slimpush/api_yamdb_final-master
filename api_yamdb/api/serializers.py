from rest_framework import serializers
from rest_framework.serializers import ValidationError

from reviews.models import Comment, Genre, Category, Title, Review, User

REGEX_NAME = r'^(?!me\Z)^[\w.@+-]+\Z'
USERNAME_FIELD = serializers.RegexField(REGEX_NAME, max_length=150)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'rating', 'name',
                  'year', 'description', 'genre', 'category')
        model = Title


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'rating', 'name',
                  'year', 'description', 'genre', 'category')
        model = Title


class UserSerializer(serializers.ModelSerializer):
    username = USERNAME_FIELD
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User

    def validate_username(self, username):
        unique_test = User.objects.filter(
            username=username
        ).exists()
        username = username.lower()
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.')
        if unique_test:
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует')
        return username

    def validate_email(self, email):
        email = email.lower()
        unique_test = User.objects.filter(
            email=email
        ).exists()
        if unique_test:
            raise serializers.ValidationError(
                'Пользователь с такой почтой уже существует')
        return email


class UserCreateSerializer(serializers.ModelSerializer):
    username = USERNAME_FIELD
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        email = data.get('email').lower()
        username = data.get('username').lower()
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.')
        if User.objects.filter(email=email, username=username).exists():
            return data
        if User.objects.filter(username=data.get('username')):
            raise ValidationError(
                'Пользователь с таким именем уже зарегистрирован'
            )
        if User.objects.filter(email=data.get('email')).exists():
            raise ValidationError('Данный email уже используется')
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = USERNAME_FIELD
    confirmation_code = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserMeSerializer(serializers.ModelSerializer):
    username = USERNAME_FIELD
    email = serializers.EmailField(max_length=254, required=True)
    last_name = serializers.CharField(max_length=150)

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'author', 'text', 'title', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'author', 'text', 'review', 'pub_date')
        model = Comment
        read_only_fields = ('review',)
