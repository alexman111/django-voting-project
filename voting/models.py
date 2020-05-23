from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_verified = models.BooleanField(verbose_name='Подтверждён', default=False)
    is_voted = models.BooleanField(verbose_name='Проголосовал', default=False)

    def vote(self):
        self.is_voted = True
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Image(models.Model):
    url = models.ImageField(upload_to="candidate_images", blank=True, null=True, verbose_name='Изображение')

    def __str__(self):
        return self.url.name


class Candidate(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя', null=True)
    surname = models.CharField(max_length=200, verbose_name='Фамилия', null=True)
    second_name = models.CharField(max_length=200, verbose_name='Отчество', null=True)

    votes = models.PositiveIntegerField(verbose_name='Количество голосов', null=True, default=0)

    biography = models.TextField(max_length=10000, verbose_name='Биография', null=True)
    election_programme = models.TextField(max_length=10000, verbose_name='Предвыборная программа', null=True)

    image = models.OneToOneField(Image, on_delete=models.CASCADE, null=True, verbose_name='Изображение')

    def inc_votes(self):
        self.votes += 1
        self.save()

    def __str__(self):
        return self.name + ' ' + self.surname

    def __eq__(self, other):
        return self.id == other.id

    class Meta:
        verbose_name = 'кандидата'
        verbose_name_plural = 'кандидат'


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария',
                               blank=True, null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, verbose_name='Кандидат',
                                  blank=True, null=True, related_name='comments_candidates')
    date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст комментария')

    def __str__(self):
        return self.text

    def __eq__(self, other):
        return self.text == other.text and self.candidate == other.candidate
