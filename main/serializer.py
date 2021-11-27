from rest_framework import serializers
from rest_framework.decorators import action

from .models import Article, CodeImage, Reply, Comment


class CodeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeImage
        fields = ('image',)

    def _get_image_url(self, obj):
        print(self.context)
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return 'http://localhost:3000' + url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ('author',)

    def create(self, validate_data):
        request = self.context.get('request')
        images_data = request.FILES
        author = request.user
        article = Article.objects.create(author=author, **validate_data)
        for image in images_data.getlist('images'):
            CodeImage.objects.create(image=image, article=article)
        return article

    def update(self, instance, validated_data):
        request = self.context.get('request')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        images_data = request.FILES
        instance.images.all().delete()
        for image in images_data.getlist('images'):
            CodeImage.objects.create(image=image, article=instance)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = CodeImageSerializer(instance.images.all(), many=True).data
        representation['replies'] = ReplySerializer(instance.replies.all(), many=True).data
        return representation


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Reply
        fields = '__all__'

        def create(self, validated_data):
            request = self.context.get('request')
            reply = Reply.objects.create(author=request.user, **validated_data)
            return reply

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
            if action == 'retrieve':
                representation['replies'] = instance.replies.count()
            else:
                representation['replies'] = ReplySerializer(instance.replies.all(), many=True).data
            print(action)
            return


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'

        def create(self, validated_data):
            request = self.context.get('request')
            comment = Comment.objects.create(author=request.user, **validated_data)
            return comment
