from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

TITLE_MAX_LENGTH = 30


class Group(models.Model):
    title = models.CharField('Группа', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title[:TITLE_MAX_LENGTH]


class Post(models.Model):
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True
                                    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/',
                              null=True,
                              blank=True
                              )
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True
                              )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:TITLE_MAX_LENGTH]


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments'
                               )
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments'
                             )
    text = models.TextField('Комментарий')
    created = models.DateTimeField('Дата добавления',
                                   auto_now_add=True,
                                   db_index=True
                                   )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return (f'{self.post} {self.author} "'
                f'{self.text[:TITLE_MAX_LENGTH]}"')
