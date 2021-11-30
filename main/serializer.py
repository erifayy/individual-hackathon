from django.db.models import Avg
from rest_framework import serializers
from rest_framework.decorators import action

from account.models import MyUser
from .models import Article, Image, Comment, Favorite, Rating


class ArticleSerializer(serializers.ModelSerializer):
    added = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('title', 'description', 'year', 'total_likes', 'is_fan', 'added')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['images'] = ImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['rating'] = instance.rating.aggregate(Avg('rating'))
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        movie = Article.objects.create(**validated_data)
        return movie

    def get_is_fan(self, obj) -> bool:
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

    def _get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return 'http://localhost:8000' + url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        reply = Comment.objects.create(author=request.user, **validated_data)
        return reply


class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email', )


class ChangePasswordSerializer(serializers.Serializer):
    model = MyUser
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['article'] = instance.article.title
        return representation


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        article = validated_data.get('article')
        rating = Rating.objects.get_or_create(user=request.user, article=article)[0]
        rating.rating = validated_data['rating']
        rating.save()
        return rating
