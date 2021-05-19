from django.shortcuts import render
from MusicBeats.models import Song,Watchlater
from django.db.models import Case,When

def index(request):
    song = Song.objects.all()[0:4]

    if request.user.is_authenticated:
        wl = Watchlater.objects.filter(user=request.user)
        ids = []
        for i in wl:
            ids.append(i.video_id)

        preserved = Case(*[When(pk=pk, then=pos) for pos,pk in enumerate(ids)])
        watch = Song.objects.filter(song_id__in=ids).order_by(preserved)
        watch = reversed(watch)
    else:
        watch = Song.objects.all()[0:4]
    
    return render(request,'index.htm',{'song': song, 'watch': watch})