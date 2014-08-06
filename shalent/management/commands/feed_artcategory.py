from django.core.management.base import BaseCommand
from Auth.models import ArtCategory

#art_category = ["Photography","Modeling","Painting","Design","Sculpting","Curate Flims","Curate Music",
#                "Radio","Curate Stories","Script","Subtitles","Synposis","Lyrics","Poem","Jokes","Literature",
#                "Novel","Articles","Biography","Blog","News","Caligraphy","Curate"]

art_category = ["Actor", "Band", "Beat Boxer", "Celebrity", "Choreographer",
    "Composer", "Dancer", "Designer", "DJ", "Film maker", "Model",
    "Music Composer", "Musician", "Party Acts", "Photographer", "Poet",
    "Producer", "RJ", "Singer", "Sound Engineer", "Stand Up Comedian",
    "Stylist", "Visual and Fine artist", "VJ", "Writer"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        ArtCategory.objects.all().delete()
        for category in art_category:
            try:
                ArtCategory(**{'category':category}).save()
            except:
                print sys.exc_info()                
