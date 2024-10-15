from django.contrib import admin
from .models import Participant, Reservation

class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 1  # Number of empty forms to display
    readonly_fields = ("reservation_date",)  # Ensure this field is displayed as read-only
    autocomplete_fields = ('participant',)  # Enable autocomplete for the participant field

class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "cin",
        "participant_category",  # Ensure this matches your model field
        "created_at",
        "updated_at",
    )
    
    search_fields = ("username", "first_name", "last_name", "email", "cin")
    list_per_page = 10
    ordering = ("created_at",)
    readonly_fields = ("created_at", "updated_at")  # Ensure these fields are read-only

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('username', 'first_name', 'last_name', 'email', 'cin', 'participant_category') 
        }),
        ('Données de suivi', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    inlines = [ReservationInline]  # Include the ReservationInline to show reservations

    list_filter = (
        'participant_category',  # Updated to match your model
        'created_at',
    )
    list_editable = ('first_name', 'last_name')

# Register the Participant model with the customized admin
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Reservation)  # Register the Reservation model as well
