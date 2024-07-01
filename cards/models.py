from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)


class Deck(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def new_count(self):
        return self.cards.filter(state='new').count()

    def learning_count(self):
        return self.cards.filter(state='learning').count()

    def review_count(self):
        return self.cards.filter(state='review', due_date__lte=timezone.now()).count()


class Card(models.Model):
    STATE_CHOICES = [
        ('new', 'New'),
        ('learning', 'Learning'),
        ('review', 'Review'),
        ('relearning', 'Relearning'),
    ]
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards', default=1)
    box = models.IntegerField(choices=zip(BOXES, BOXES), default=BOXES[0])
    original_box = models.IntegerField(choices=zip(BOXES, BOXES), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='new')
    due_date = models.DateTimeField(default=datetime.now)
    last_review = models.DateTimeField(null=True, blank=True)
    reps = models.IntegerField(default=0)
    elapsed_days = models.IntegerField(default=0)
    difficulty = models.FloatField(default=0.0)
    stability = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.question

    def move(self, solved):
        new_box = self.box + 1 if solved else BOXES[0]

        if new_box in BOXES:
            self.box = new_box
            self.save()
        return self
    
    def archive(self):
        self.original_box = self.box
        self.archived = True
        self.save()

    def unarchive(self):
        if self.original_box is not None:
            self.box = self.original_box
        self.archived = False
        self.original_box = None
        self.save()

    def update_due_date(self, rating):
        # Update the due date based on the user's rating
        if rating == 'again':
            self.due_date = timezone.now() + timedelta(days=1)  # Repeat the next day
        elif rating == 'hard':
            self.due_date = timezone.now() + timedelta(days=3)  # Review again in 3 days
        elif rating == 'good':
            self.due_date = timezone.now() + timedelta(days=7)  # Review again in a week
        elif rating == 'easy':
            self.due_date = timezone.now() + timedelta(days=14)  # Review again in two weeks
        self.last_review = timezone.now()  # Update the last review time
        self.save()