from django.shortcuts import render

from .models import User

from .utils import checkPasswordMatches, checkPasswordSecurity

# Create your views here.

def register(request):
    #username = request.POST["username"]
    username = "Pepe"
    #password = request.POST["password"]
    #repPassword = request.POST["repPassword"]

    password = "1234Antoni"
    repPassword = "1234Antoni"

    # First check if the username is already logged in
    context = {

    }

    user = User.objects.filter(Username=username)

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
                
                user = User(Username=username, Password=password)

                user.save()
                
                pass  
            else:
                print("Las contraseñas no son iguales!")
                #La contraseña no es igual, porfavor vuelva!
                pass
        else:
            #La contraseña no es segura!
            print("Contraseña " + password + " no es segura!")
            pass

    return render(request, 'index.html', context)

def login():
    pass


