from django import template

from cards.models import BOXES, Card, Deck

register = template.Library()


@register.inclusion_tag("cards/box_links.html", takes_context=True)
def boxes_as_links(context, deck):
    boxes = []
    for box_num in BOXES:
        card_count = Card.objects.filter(deck=deck, box=box_num, archived=False).count()
        boxes.append({
            "number": box_num, 
            "card_count": card_count,
        })
    archive_count = Card.objects.filter(deck=deck, archived=True).count()
    return {"boxes": boxes, "archive_count": archive_count, "deck_id": deck.id}