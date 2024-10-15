from django.db import models
from categories.models import Category
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

class Conference(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now)  # Corrected this line
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.FloatField()
    capacity = models.IntegerField(
        validators=[MaxValueValidator(limit_value=800, message="Capacity must be less than 800")]
    )
    program = models.FileField(
        upload_to='files/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf','png'], message="Only PDF allowed")]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Changed this to update the field when a record is modified
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="conferences")

    def clean(self):
        # Ensure end_date is after start_date
        if self.end_date < self.start_date:
            raise ValidationError("The end date must be after the start date.")

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_date__gte=timezone.now().date()),
                name="the_start_date_must_be_greater_or_equal_than_today_time"
            )
        ]

    def __str__(self):
        return f"title conference = {self.title}"
