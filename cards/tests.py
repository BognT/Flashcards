from django.test import TestCase
from django.urls import reverse
from .models import Card

class CardArchiveTest(TestCase):
    def setUp(self):
        self.card = Card.objects.create(
            question='Test Question',
            answer='Test Answer',
            box=1
        )

    def test_archive_card(self):
        response = self.client.post(reverse('card-archive', kwargs={'pk': self.card.pk}))
        self.assertEqual(response.status_code, 302)  # Check for redirect after archive

        archived_card = Card.objects.get(pk=self.card.pk)
        self.assertTrue(archived_card.archived)

    def test_unarchive_card(self):
        self.card.archived = True
        self.card.save()

        response = self.client.post(reverse('card-unarchive', kwargs={'pk': self.card.pk}))
        self.assertEqual(response.status_code, 302)  # Check for redirect after unarchive

        unarchived_card = Card.objects.get(pk=self.card.pk)
        self.assertFalse(unarchived_card.archived)
