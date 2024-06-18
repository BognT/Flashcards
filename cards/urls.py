from django.test import TestCase
from django.urls import reverse
from .models import Card


class TestCardViews(TestCase):
    def setUp(self):
        self.card = Card.objects.create(question="Test Question", answer="Test Answer", box=1)

    def test_create_card_view(self):
        url = reverse('card-create')
        data = {
            'question': 'Test Question',
            'answer': 'Test Answer',
            'box': 1
        }
        response = self.client.post(url, data, follow=True)
        self.assertIn(b'Card "Test Question" created successfully.', response.content)

    def test_update_card_view(self):
        url = reverse('card-update', args=[self.card.id])
        data = {
            'question': 'Updated Question',
            'answer': 'Updated Answer',
            'box': 2  # or any box number you want to test
        }
        response = self.client.post(url, data, follow=True)
        self.assertIn(b'Card "Updated Question" updated successfully.', response.content)

    def test_archive_card_view(self):
        url = reverse('card-archive', args=[self.card.id])
        response = self.client.post(url, {}, follow=True)
        self.assertIn(b'Card "{self.card.question}" archived.', response.content)

    def test_unarchive_card_view(self):
        url = reverse('card-unarchive', args=[self.card.id])
        response = self.client.post(url, {}, follow=True)
        self.assertIn(b'Card "{self.card.question}" unarchived.', response.content)

    def test_move_card_view(self):
        url = reverse('box', args=[self.card.box])
        response = self.client.get(url, follow=True)
        self.assertIn(bytes(f'{self.card.question}', 'utf-8'), response.content)
