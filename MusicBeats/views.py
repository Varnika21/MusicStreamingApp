from django.shortcuts import redirect, render
from MusicBeats.models import Song,Watchlater,History,Channel
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
        redirect('/')

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


def logout_user(request):
    logout(request)
    return redirect("/")

def channel(request,channel):
    chan = Channel.objects.filter(name=channel).first()
    return render(request,"MusicBeats/channel.htm",{'channel' : chan})


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


    return render(request,"MusicBeats/upload.htm")