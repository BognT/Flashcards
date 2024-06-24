from django.db import models

NUM_BOXES = 5
BOXES = range(1, NUM_BOXES + 1)


class Deck(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Card(models.Model):
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='cards', default=1)
    box = models.IntegerField(choices=zip(BOXES, BOXES), default=BOXES[0])
    original_box = models.IntegerField(choices=zip(BOXES, BOXES), null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

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
