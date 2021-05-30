from django.shortcuts import redirect, render
from MusicBeats.models import Song,Watchlater,History,Channel,Favourites
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.db.models import Case,When

def history(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id']
        history = History(user=user, music_id=music_id)
        history.save()
        return redirect(f"/MusicBeats/songs/{music_id}")
    
    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos,pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)
    
    return render(request, 'MusicBeats/history.htm',{'history': song})

def watchlater(request):
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']

        watch = Watchlater.objects.filter(user=user)
        
        for i in watch:
            if video_id == i.video_id:
                message = "Your song is already added"
                break
        else:                   
            watchlater = Watchlater(user = user, video_id = video_id)
            watchlater.save()
            message = "Your song is Successfully added"

    
    
        song = Song.objects.filter(song_id = video_id).first()
        return render(request,f"MusicBeats/songpost.htm",{'song': song, "message": message})
    
    wl = Watchlater.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos,pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request,"MusicBeats/Watchlater.htm", {'song': song})
def favourites(request):
    if request.method == "POST":
        user = request.user
        fav_song_id = request.POST['fav_song_id']

        fav = Favourites.objects.filter(user=user)
        
        for i in fav:
            if fav_song_id == i.fav_song_id:
                message = "Your song is already added"
                break
        else:                   
            favourites = Favourites(user = user, fav_song_id = fav_song_id)
            favourites.save()
            message = "Your song is added to favourites"

    
    
        song = Song.objects.filter(song_id = fav_song_id).first()
        return render(request,f"MusicBeats/songpost.htm",{'song': song, "message": message})
    
    f1 = Favourites.objects.filter(user=request.user)
    ids = []
    for i in f1:
        ids.append(i.fav_song_id)

    preserved = Case(*[When(pk=pk, then=pos) for pos,pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request,"MusicBeats/Favourites.htm", {'song': song})
    


def songs(request):
    song = Song.objects.all()
    return render(request,'MusicBeats/songs.htm',{'song' : song})
def songpost(request, id):
    song = Song.objects.filter(song_id = id).first()
    return render(request,'MusicBeats/songpost.htm',{'song' : song})
def login(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password )
        from django.contrib.auth import login
        login(request, user)
        return redirect('/')

    return render(request,'MusicBeats/login.htm')

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        user = authenticate(username=username, password=pass1)
        from django.contrib.auth import login
        login(request, user)

        channel = Channel(name = username)
        channel.save()

        return redirect('/')
    return render(request,'MusicBeats/signup.htm')

def search(request):
    query = request.GET.get("query")
    song = Song.objects.all()

    qs = song.filter(name__icontains = query)

    return render(request,"MusicBeats/search.htm",{"songs" : qs,"query" : query})


def logout_user(request):
    logout(request)
    return redirect("/")

def channel(request,channel):
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.music).split(" ")[1:]

    preserved = Case(*[When(pk=pk, then=pos) for pos,pk in enumerate(video_ids)])
    song = Song.objects.filter(song_id__in=video_ids).order_by(preserved)

    return render(request,"MusicBeats/channel.htm",{'channel' : chan, 'song' : song})


def upload(request):
    if request.method == "POST":
        name = request.POST['name']
        singer = request.POST['singer']
        movie = request.POST['movie']
        genre = request.POST['genre']
        credit = request.POST['credit']
        image = request.POST['image']
        song1 = request.FILES['file']

        song_model = Song(name = name,image = image,singer = singer,genre = genre,movie = movie,credit = credit,song = song1)
        song_model.save()

        music_id = song_model.song_id
        channel_find = Channel.objects.filter(name = str(request.user))

        for i in channel_find:
            i.music += f" {music_id}"
            i.save()


    return render(request,"MusicBeats/upload.htm")