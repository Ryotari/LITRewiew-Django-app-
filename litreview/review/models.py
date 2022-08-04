from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from PIL import Image
from authentication.models import User

class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (400, 400)
    
    def resize_image(self):

        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # sauvegarde de l’image redimensionnée dans le système de fichiers
        # ce n’est pas la méthode save() du modèle !
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def give_permissions_to_creator(self):

        user = User.objects.get(username=self.user)
        permission = Permission.objects.get(codename='change_ticket')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='delete_ticket')
        user.user_permissions.add(permission)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.give_permissions_to_creator()

class Review(models.Model):

    class Rating(models.TextChoices):
        ONE_STAR = 'One Star'
        TWO_STARS = 'Two Stars'
        THREE_STARS = 'Three Stars'
        FOUR_STARS = 'Four Stars'
        FIVE_STARS = 'Five Stars'

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.fields.CharField(choices=Rating.choices, max_length=20)
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def give_permissions_to_creator(self):

        user = User.objects.get(username=self.user)
        permission = Permission.objects.get(codename='change_review')
        user.user_permissions.add(permission)
        permission = Permission.objects.get(codename='delete_review')
        user.user_permissions.add(permission)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.give_permissions_to_creator()

class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followed_by')

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user', )
