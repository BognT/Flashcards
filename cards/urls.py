from django.urls import path
from . import views
from .views import (
    DeckListView, DeckCreateView, DeckUpdateView, DeckDeleteView, CardListView, CardCreateView, CardUpdateView, BoxView,
    ArchiveCardView, ArchivedCardListView, UnarchiveCardView
)

urlpatterns = [
    path("", DeckListView.as_view(), name="deck-list"),
    path("deck/<int:deck_id>/", CardListView.as_view(), name="card-list"),
    path("deck/<int:deck_id>/create/", CardCreateView.as_view(), name="card-create"),
    path("deck/<int:deck_id>/update/<int:pk>/", CardUpdateView.as_view(), name="card-update"),
    path("deck/<int:deck_id>/box/<int:box_num>/", BoxView.as_view(), name="box"),
    path("deck/<int:deck_id>/archive/<int:pk>/", ArchiveCardView.as_view(), name="card-archive"),
    path("deck/<int:deck_id>/archived/", ArchivedCardListView.as_view(), name="archived-cards"),
    path("deck/<int:deck_id>/unarchive/<int:pk>/", UnarchiveCardView.as_view(), name="card-unarchive"),
    path("deck/create/", DeckCreateView.as_view(), name="deck-create"),
    path("deck/<int:pk>/edit/", DeckUpdateView.as_view(), name="deck-edit"),
    path("deck/<int:pk>/delete/", DeckDeleteView.as_view(), name="deck-delete"),
    path('deck/<int:deck_id>/study/', views.study_now, name='study-now'),
    path('deck/<int:deck_id>/record_answer/<int:card_id>/<str:rating>/', views.record_answer, name='record-answer'),
]
