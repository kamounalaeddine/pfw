from django.contrib import admin
from django.utils import timezone
from .models import Conference
from users.models import Reservation
from django.db import models  # Import models from django.db


class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 1
    readonly_fields = ("reservation_date",)  # Assurez-vous que cette colonne existe

class ParticipantsFilter(admin.SimpleListFilter):
    title = 'Participants'  # Titre du filtre
    parameter_name = 'participants'  # Nom du paramètre dans l'URL

    def lookups(self, request, model_admin):
        return (
            ('no_participants', 'No participants'),
            ('has_participants', 'There are participants'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no_participants':
            return queryset.filter(reservations__isnull=True)
        elif self.value() == 'has_participants':
            return queryset.filter(reservations__isnull=False)
        return queryset

class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "start_date", "end_date", "price")
    search_fields = ("title",)
    list_per_page = 10 
    ordering = ("start_date",)
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        ('Description', {
            'fields': ('title', 'description', 'category')
        }),
        ('Horaires de la conférence', {
            'fields': ('start_date', 'end_date')
        }),
        ('Localisation et détails', {
            'fields': ('location', 'price', 'capacity')
        }),
        ('Programme', {
            'fields': ('program',)
        }),
        ('Données de suivi', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    inlines = [ReservationInline]
    autocomplete_fields = ('category',)

    # Ajout des filtres
    list_filter = (
        'title',  # Filtre selon le titre de la conférence
        ParticipantsFilter,  # Filtre personnalisé pour le nombre de participants
        'start_date',  # Filtre pour la date de la conférence
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Ajout d'un filtre personnalisé pour les dates
        queryset = queryset.annotate(
            is_today=models.Case(
                models.When(start_date=timezone.now().date(), then=True),
                default=False,
                output_field=models.BooleanField(),
            )
        )
        return queryset

    def past_conferences(self, request, queryset):
        return queryset.filter(start_date__lt=timezone.now())

    def upcoming_conferences(self, request, queryset):
        return queryset.filter(start_date__gt=timezone.now())

    def today_conferences(self, request, queryset):
        return queryset.filter(start_date=timezone.now().date())

    def today_conferences(self, request, queryset):
        return queryset.filter(start_date=timezone.now().date())

# Enregistrement des modèles dans l'admin
admin.site.register(Conference, ConferenceAdmin)
