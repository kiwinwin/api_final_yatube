from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F

User = get_user_model()


class Group(models.Model):
    title = models.CharField('Название группы', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        ordering = ('id',)
        verbose_name = 'группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.id


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', null=True, blank=True,
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    following = models.ForeignKey(User, on_delete=models.SET_NULL,
                                  related_name='followers',
                                  null=True, blank=True,)

    class Meta:

        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following', ),
                name='It should be unique set',),
            models.CheckConstraint(
                check=~models.Q(user=F('following')),
                name='FollowingYourself',),
        )

    def __str__(self):
        return {self.user}
