from django.contrib import admin
from .models import Deck, Card

# Register Deck model
@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Register Card model
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'deck', 'box', 'original_box', 'date_created', 'archived')
    search_fields = ('question', 'answer', 'deck__name')
    list_filter = ('deck', 'box', 'archived')
    ordering = ('date_created',)
