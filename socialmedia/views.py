from django.shortcuts import render, redirect

from .utils import checkPasswordMatches, checkPasswordSecurity
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

# Create your views here.


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if(signUpUser(**form.cleaned_data)):
                print("Something went bad!")
                return redirect('/login/')
            else:
                print("User logged in!")
                return redirect('/register/')
               
          
            
    context = {
       'form' : form 
    }
    return render(request, 'auth.html', context)



def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            
            if(loginUser(**form.cleaned_data)):
                username = form.cleaned_data["username"]
                print("Usuario logeado")
                return redirect('/home/' + username)
            else:
                print("Este usuario no existe!")
                return redirect('/login/')

                  
          
    context = {
       'form' : form 
    }
    return render(request, 'auth.html', context)

def signUpUser(username, password, repPassword):
    user = User.objects.filter(username=username)

    if user.__len__() > 0:
        print("User is already created!")
    
    else:
        print("User is not created, go on!")
        #Check password security
        if(checkPasswordSecurity(password)):
            print("Contraseña segura!")
            #Check if password matches!
            if(checkPasswordMatches(password, repPassword)):
                print("Las contraseñas son iguales!")
                #La contraseña es igual, creamos usuario
                
                user = User(username=username, password=password)

                user.save()
                
                return True
            else:
                print("Las contraseñas no son iguales!")
                #La contraseña no es igual, porfavor vuelva!
                return False
        else:
            #La contraseña no es segura!
            print("Contraseña " + password + " no es segura!")
            return False 

def loginUser(username, password):
    user = User.objects.filter(username=username).only()

    if(user.__len__() > 0):
        print("User exists")
        if(password == user[0].password):
            return True
        else:
            return False
    else:
        return False

    

def home(request, username):
    print(username)
    context = {
       'user': {
           'username' : username
       }
    }
    return render(request, 'home.html', context)
     



