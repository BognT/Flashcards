from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
import random

from .forms import CardCheckForm
from .models import Card


class CardListView(ListView):
    model = Card
    queryset = Card.objects.filter(archived=False).order_by("box", "-date_created")


class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer", "box"]
    success_url = reverse_lazy("card-create")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Card "{form.instance.question}" created successfully.')
        return response


class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy("card-list")

    def form_valid(self, form):
        response = super(CardCreateView, self).form_valid(form)
        messages.success(self.request, f'Card "{form.instance.question}" updated successfully.')
        return response

class BoxView(CardListView):
    template_name = "cards/box.html"
    form_class = CardCheckForm

    def get_queryset(self):
        return Card.objects.filter(box=self.kwargs["box_num"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["box_number"] = self.kwargs["box_num"]
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
        return redirect('card-list')
    
class ArchivedCardListView(ListView):
    model = Card
    template_name = "cards/archived_cards.html"
    queryset = Card.objects.filter(archived=True).order_by("-date_created")

class UnarchiveCardView(View):

    def post(self, request, pk, *args, **kwargs):
        card = get_object_or_404(Card, pk=pk)
        card.unarchive()
        messages.success(request, f'Card "{card.question}" unarchived.')
        return redirect('archived-cards')
