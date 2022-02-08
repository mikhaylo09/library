from django.db.models import signals
from django.dispatch import receiver
from .models import Review, Book
from django.db.models import Avg

@receiver(signals.post_save, sender=Review)
def create_review(sender, instance, **kwargs):
    rating = Review.objects.filter(book_id=instance.book_id).aggregate(avg_rating=Avg('rate'))
    print(rating)
    Book.objects.filter(id=instance.book_id).update(rating = rating['avg_rating'])