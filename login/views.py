
from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages
from time import gmtime, strftime
import bcrypt

from .models import User, Poke, Poke2

# Create your views here.
def login(request):
    return render(request, 'registro.html')
def registrar(request):
    return render(request, 'registro.html')

def inicio(request):
    usuario = User.objects.filter(email=request.POST['email2'])
    errores = User.objects.validar_login(request.POST, usuario)

def inicio2(request):
    email2=request.POST['email2']
    gato=request.POST['gato']
    password=request.POST['password']
    
    #creacion en base de datos del poke
    poke = Poke.objects.create(
        email = email2,
        gato = gato,
        password = password,
        
    )
    
    #lista_pokes = Poke.objects.all()

    #busco  desde la base de datos todos los pokes
    #return HttpResponse(email2+" "+gato+" "+password)

    #pasando data a Front   
    context={
        'gato':request.POST,
        'elefante':gato,
        'avion':password,
        'lista_pokes': Poke.objects.all()
    }

    return render(request, 'prueba.html',context)


def inicio3(request):
    nombre = request.POST['nom']
    edad = request.POST['edad']
    mail = request.POST['mail']
    
    poke2 = Poke2.objects.create(
        nombre = nombre,
        edad = edad,
        mail = mail, 
    )
    
    context={
        'leon':nombre,
        'tigre':edad,
        'puma': mail,
    }
    
    return render(request, 'mostrar.html',context)
    
    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg)
        return redirect('/')
    else:
        request.session['user_id'] = usuario[0].id
        return redirect('home/')

def registro(request):
    #validacion de parametros
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg)
        return redirect('/registrar')

    else:
        #encriptar password
        password = User.objects.encriptar(request.POST['password'])
        decode_hash_pw = password.decode('utf-8')
        #crear usuario
        if request.POST['rol'] == '1':
            user = User.objects.create(
                nombre=request.POST['nombre'],
                alias=request.POST['alias'],
                email=request.POST['email'],
                cumple=request.POST['cumple'],
                password=decode_hash_pw,
                rol=1,
            )
        else:
            user = User.objects.create(
                nombre=request.POST['nombre'],
                alias=request.POST['alias'],
                email=request.POST['email'],
                password=decode_hash_pw,
                rol=2,
            )
        request.session['user_id'] = user.id
    return redirect('home/')

def logout(request):
    request.session.flush()
    return redirect('/')