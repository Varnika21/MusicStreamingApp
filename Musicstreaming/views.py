from django.shortcuts import render
from MusicBeats.models import Song
def index(request):
    song = Song.objects.all()[0:4]
    return render(request,'index.htm',{'song': song})