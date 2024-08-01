from rest_framework import serializers

from posts.models import Comment, Post, Group, Follow, User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    image = serializers.StringRelatedField()
    comments = CommentSerializer

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('pub_date',)


class FollowSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(queryset=User.objects.all(),
                                             slug_field='username')

    class Meta:
        fields = '__all__'
        model = Follow

        '''validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'))]'''

    '''def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError('Sorry, you can not follow yourself.')
        return value'''
