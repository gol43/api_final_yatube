from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from posts.models import Group, Post, Comment, Follow, User
# Не понимаю, для чего было убирать серилизатор для Group из git clone,
# если в предыдущем спринте было то же самое
from rest_framework.validators import UniqueTogetherValidator


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
# Что касается CurrentUserDefault:
# Я нашёл в документации django-rest-framework обьяснение проблемы
# с получением юзера
# Но в этой же документации ещё использовалось HiddenField
# Я всячески пытался применить с ним, но никак не получалось и pytest ругался
# В итоге оставил просто default. Видел, что ребята из Пачки также делали
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        queryset = Follow.objects.all()
        fields_for_val = ('user', 'following')
        message = 'Yoo, man, u did that already'
        validators = [UniqueTogetherValidator(
            queryset, fields_for_val, message)
        ]
        model = Follow
        fields = '__all__'
# Что касается UniqueTogetherValidator:
# Я также взял из той же документации
# Увидел ошибку в pytest и тем самым наложил некоторое ограничение на поля

    def validate_following(self, data):
        self.request = self.context['request']
        self.user = self.request.user
        message = 'Name the Error: You cant be follower'
        if self.user == data:
            raise serializers.ValidationError(message)
        return data
