from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Card, Deck
from fsrs import FSRS, Card as FSRSCard, Rating
import random
import logging


from .forms import CardCheckForm, DeckForm
from .models import Card, Deck

class DeckListView(ListView):
    model = Deck
    template_name = "cards/deck_list.html"
    context_object_name = "deck_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = None
        return context    

class DeckCreateView(CreateView):
    model = Deck
    form_class = DeckForm
    template_name = "cards/deck_form.html"
    success_url = "/"

    def get_success_url(self):
        return reverse_lazy("deck-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Deck "{form.instance.name}" created successfully.')
        return response
    
class DeckUpdateView(UpdateView):
    model = Deck
    form_class = DeckForm
    template_name = "cards/deck_form.html"
    success_url = reverse_lazy("deck-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = self.object
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Deck "{form.instance.name}" updated successfully.')
        return response
    
class DeckDeleteView(DeleteView):
    model = Deck
    success_url = reverse_lazy("deck-list")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Deck deleted successfully.")
        return response

class CardListView(ListView):
    model = Card
    template_name = "cards/card_list.html"
    context_object_name = "card_list"

    def get_queryset(self):
        self.deck = get_object_or_404(Deck, id=self.kwargs['deck_id'])
        return Card.objects.filter(deck=self.deck, archived=False).order_by("box", "-date_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck = get_object_or_404(Deck, pk=self.kwargs['deck_id'])
        context['deck'] = deck
        context['card_list'] = Card.objects.filter(deck=deck)
        return context

class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer", "box"]

    def get_success_url(self):
        return reverse_lazy("card-list", kwargs={'deck_id': self.kwargs['deck_id']})

    def form_valid(self, form):
        form.instance.deck = get_object_or_404(Deck, id=self.kwargs['deck_id'])
        response = super().form_valid(form)
        messages.success(self.request, f'Card "{form.instance.question}" created successfully.')
        return response

    def get_success_url(self):
        return reverse_lazy('card-list', kwargs={'deck_id': self.kwargs['deck_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = get_object_or_404(Deck, id=self.kwargs['deck_id'])
        return context

class CardUpdateView(CardCreateView, UpdateView):
    
    def get_success_url(self):
        return reverse_lazy("card-list", kwargs={'deck_id': self.object.deck.id})

    def form_valid(self, form):
        response = super(CardCreateView, self).form_valid(form)
        messages.success(self.request, f'Card "{form.instance.question}" updated successfully.')
        return response

class BoxView(CardListView):
    template_name = "cards/box.html"
    form_class = CardCheckForm

    def get_queryset(self):
        self.deck = get_object_or_404(Deck, id=self.kwargs['deck_id'])
        return Card.objects.filter(deck=self.deck, box=self.kwargs["box_num"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["box_number"] = self.kwargs["box_num"]
        context['deck'] = self.deck
        context['deck_id'] = self.deck.id
        if self.object_list:
            context["check_card"] = random.choice(self.object_list)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            card = get_object_or_404(Card, id=form.cleaned_data["card_id"])
            old_box = card.box
            card.move(form.cleaned_data["solved"])
            messages.success(request, f'Card "{card.question}" moved from Box {old_box} to Box {card.box}.')
        return redirect(request.META.get("HTTP_REFERER"))
    
class ArchiveCardView(View):

    def post(self, request, pk, *args, **kwargs):
        card = get_object_or_404(Card, pk=pk)
        card.archived = True
        card.save()
        messages.success(request, f'Card "{card.question}" archived.')
        return redirect('card-list', deck_id=card.deck.id)
    
class ArchivedCardListView(ListView):
    model = Card
    template_name = "cards/archived_cards.html"

    def get_queryset(self):
        self.deck = get_object_or_404(Deck, id=self.kwargs['deck_id'])
        return Card.objects.filter(deck=self.deck, archived=True).order_by("-date_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['deck'] = self.deck
        context['deck_id'] = self.deck.id
        return context

class UnarchiveCardView(View):

    def post(self, request, pk, *args, **kwargs):
        card = get_object_or_404(Card, pk=pk)
        card.unarchive()
        messages.success(request, f'Card "{card.question}" unarchived.')
        return redirect('archived-cards', deck_id=card.deck.id)

fsrs = FSRS()

def study_now(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    now = timezone.now()
    cards = deck.cards.filter(archived=False, due_date__lte=now).order_by('due_date')
    if not cards:
        return render(request, 'cards/no_cards_to_study.html')
    
    card = cards.first()
    return render(request, 'cards/study_now.html', {'card': card, 'deck': deck})

logger = logging.getLogger(__name__)

def record_answer(request, deck_id, card_id, rating):
    card = get_object_or_404(Card, pk=card_id)
    deck = card.deck
    now = timezone.now()

    if not card.last_review:
        card.last_review = card.date_created
    
    fsrs_card = FSRSCard(state=card.state, due=card.due_date, last_review=card.last_review)
    rating_mapping = {
        'again': Rating.Again,
        'hard': Rating.Hard,
        'good': Rating.Good,
        'easy': Rating.Easy,
    }
    if rating not in rating_mapping:
        return redirect('study-now', deck_id=deck_id)

    scheduling_cards = fsrs.repeat(fsrs_card, now)
    selected_card = scheduling_cards[rating_mapping[rating]].card
    
    logger.debug(f'Updated card {card_id}: state={selected_card.state}, due_date={selected_card.due}')

    card.state = selected_card.state
    card.due_date = selected_card.due
    card.last_review = now
    card.save()

    return redirect('study-now', deck_id=deck_id)