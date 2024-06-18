from django.test import TestCase
from django.urls import reverse
from .models import Card

class TestCardViews(TestCase):

    def setUp(self):
        self.card = Card.objects.create(question='Initial Question', answer='Initial Answer', box=1)

    def test_create_card_view(self):
        url = reverse('new_card')
        data = {
            'question': 'Test Question',
            'answer': 'Test Answer',
            'box': 1,
        }
        response = self.client.post(url, data, follow=True)
        self.assertIn(b'Card "Test Question" created successfully.', response.content)

    def test_update_card_view(self):
        url = reverse('edit_card', args=[self.card.id])
        data = {
            'question': 'Updated Question',
            'answer': 'Updated Answer',
            'box': 2,
        }
        response = self.client.post(url, data, follow=True)
        self.assertIn(b'Card "Updated Question" updated successfully.', response.content)

    def test_archive_card_view(self):
        url = reverse('archive_card', args=[self.card.id])
        response = self.client.post(url, follow=True)
        self.assertIn(bytes(f'Card "{self.card.question}" archived.', 'utf-8'), response.content)

    def test_unarchive_card_view(self):
        card = Card.objects.create(question='To be Unarchived', answer='To be Unarchived', box=1, archived=True)
        url = reverse('unarchive_card', args=[card.id])
        response = self.client.post(url, follow=True)
        self.assertIn(bytes(f'Card "{card.question}" unarchived.', 'utf-8'), response.content)

    def test_move_card_view(self):
        url = reverse('move_card', args=[self.card.id])
        data = {
            'box': 2,
        }
        response = self.client.post(url, data, follow=True)
        self.assertIn(bytes(f'Card "{self.card.question}" moved to box 2.', 'utf-8'), response.content)
