from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect
import random

from .forms import CardCheckForm

from .models import Card


class CardListView(ListView):
    model = Card
    queryset = Card.objects.filter(archived=False).order_by("box", "-date_created")


class CardCreateView(CreateView):
    model = Card
    fields = ["question", "answer", "box"]
    succes_url = reverse_lazy("card-create")


class CardUpdateView(CardCreateView, UpdateView):
    success_url = reverse_lazy("card-list")


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
            card.move(form.cleaned_data["solved"])

        return redirect(request.META.get("HTTP_REFERER"))
    
class ArchiveCardView(View):

    def post(self, request, pk, *args, **kwargs):
        card = get_object_or_404(Card, pk=pk)
        card.archived = True
        card.save()
        return redirect('card-list')
    
class ArchivedCardListView(ListView):
    model = Card
    template_name = "cards/archived_cards.html"
    queryset = Card.objects.filter(archived=True).order_by("-date_created")

class UnarchiveCardView(View):

    def post(self, request, pk, *args, **kwargs):
        card = get_object_or_404(Card, pk=pk)
        card.unarchive()
        return redirect('archived-cards')