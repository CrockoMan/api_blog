from datetime import datetime

from rest_framework import serializers

from posts.models import Comment, Group, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,slug_field='username')

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')

    # def create(self, validated_data):
    #     if not validated_data.get('author'):
    #         user = self.context['request'].user
    #         validated_data['author'] = user
    #         # validated_data['author'] = 1
    #     if not validated_data.get('pub_date'):
    #         validated_data['pub_date'] = datetime.now()
    #     if not validated_data.get('image'):
    #         validated_data['image'] = None
    #     return Post.objects.create(**validated_data)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,slug_field='username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
