from django.db import models
from django.contrib.auth.models import AbstractUser
from conferences.models import Conference
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


def email_validator(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError('Email must ends with @esprit.tn')

class Participant(AbstractUser):
    cin_validator = RegexValidator(
        regex=r'^\d{8}$',
        message="CIN must be exactly 8 digits long."
    )
    cin = models.CharField(primary_key=True, max_length=10, validators=[cin_validator])
    email = models.EmailField(unique=True, max_length=255, validators=[email_validator])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(unique=True, max_length=255)
    
    USERNAME_FIELD = 'username'
    
    CHOICES = (
        ('etudiant', 'etudiant'),
        ('chercheur', 'chercheur'),
        ('docteur', 'docteur'),
        ('enseignant', 'enseignant'),
    )
    participant_category = models.CharField(max_length=255, choices=CHOICES)  # Corrected field name
    Reservations = models.ManyToManyField(Conference, through='Reservation', related_name='reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Changed to auto_now for updates
    
    class Meta:
        verbose_name_plural = "Participants"

class Reservation(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    reservation_date = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.conference.start_date < timezone.now().date():
            raise ValidationError("You can only reserve for upcoming conferences")
        reservation_count = Reservation.objects.filter(participant=self.participant, reservation_date=self.reservation_date).count()  # Use count() for comparison
        if reservation_count >= 3:
            raise ValidationError("You can only make up to 3 reservations per day")

    class Meta:
        unique_together = ('conference', 'participant')
        verbose_name_plural = "Reservations"
