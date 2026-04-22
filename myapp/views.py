from django.shortcuts import render,redirect
from myapp.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request,'pagess/home.html')


@login_required(login_url='login')
def anime(request):
    if request.method == 'POST':
        data = request.POST
        
        anime_name = data.get('name')
        anime_description = data.get('description')
        anime_image = request.FILES.get('image')
        
        print(anime_name,anime_image,anime_description)
        
        Anime.objects.create(
            anime_name = anime_name,
            anime_description = anime_description,
            anime_image = anime_image
        )
        
        return redirect('anime')
        
    all_anime_data = Anime.objects.all()
    
    context = {'all_anime_data':all_anime_data}
        
    return render(request,'pagess/anime.html',context)

@login_required(login_url='login')
def anime_delete(request,id):
    
    Anime.objects.filter(id=id).delete()
    
    return redirect('anime')

@login_required(login_url='login')
def update_anime(request,id):
    querySet = Anime.objects.get(id=id)
    print(querySet)
    if request.method == 'POST':
        data = request.POST
        querySet.anime_name = data.get('name')
        querySet.anime_description = data.get('description')
        
        if request.FILES.get('anime_image'):
            querySet.anime_image = request.FILES.get('image')
        
        querySet.save()

        return redirect('anime')
    context = {'animes':querySet}
     
    return render(request,'pagess/update.html',context)


def register_user(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')    
        
        user = User.objects.filter(username=username)
        
        if(user.exists()):
            messages.info(request,"User Already Exists")
            return redirect('register')
        
        user = User.objects.create(
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            username = data.get('username'),
            password = data.get('password')      
        )
        
        user.set_password(password)
        user.save()
        messages.info(request,'Registered successful ✅')
        return redirect('register')
        
        
    return render(request,'pagess/register.html')

def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 🔒 Check empty fields
        if not username or not password:
            messages.warning(request, "All fields are required ⚠️")
            return redirect('login')

        # 🔑 Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password ❌")
            return redirect('login')

        # ✅ Login user
        login(request, user)
        return redirect('anime')

    return render(request, 'pagess/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')
