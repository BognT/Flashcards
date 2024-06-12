from . import views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.CardListView.as_view(), name="card-list"),
    path("new", views.CardCreateView.as_view(), name="card-create"),
    path("edit/<int:pk>", views.CardUpdateView.as_view(), name="card-update"),
    path("box/<int:box_num>", views.BoxView.as_view(), name="box"),
    path("archive/<int:pk>", views.ArchiveCardView.as_view(), name="card-archive"),
    path("archived", views.ArchivedCardListView.as_view(), name="archived-cards"),  # New URL pattern for archived cards
    path("unarchive/<int:pk>", views.UnarchiveCardView.as_view(), name="card-unarchive"),  # New URL pattern for unarchiving
]
