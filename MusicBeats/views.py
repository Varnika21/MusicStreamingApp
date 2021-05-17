from django.shortcuts import redirect,render
from MusicBeats.models import Song,Watchlater
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
def watchlater(request):
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']

        watch = Watchlater.objects.filter(user = user)

        for i in watch:
            if video_id == i.video_id:
                message = "This song is already added"
                break
            else:
                watchlater = Watchlater(user = user, video_id = video_id)
                watchlater.save()
                message = "This song is successfully added"
            
            song = Song.objects.filter(song_id = video_id).first()
            return render(request,f"MusicBeats/songpost.htm",{'song': song, "message": message})
    return render(request,"MusicBeats/Watchlater.htm")
def songs(request):
    song = Song.objects.all()
    return render(request,'MusicBeats/songs.htm',{'song': song})
def songpost(request,id):
    song = Song.objects.filter(song_id = id).first()
    return render(request,'MusicBeats/songpost.htm',{'song': song})
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        from django.contrib.auth import login
        login(request,user)
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
        user = authenticate(username = username, password = pass1)
        from django.contrib.auth import login
        login(request,user)
        
        return redirect('/')
    return render(request,'MusicBeats/signup.htm')