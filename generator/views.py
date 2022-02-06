from django.shortcuts import render
from django.http import HttpResponse
import random

import generator

def home(request):
    return render(request, 'generator/home.html')

def about(request):
    return render(request, 'generator/about.html')

def password(request):

    characters = list('abcdefghijklmnoprstuwzxyz')
    characters_upper = list('abcdefghijklmnoprstuwzxyz'.upper())
    nums = list('1234567890')
    specials = list('!?%$#*&@-_/.,')
    lenght = int(request.GET.get('lenght', 12))
    thepassword = ''
    uppercase = request.GET.get('uppercase')
    numbers = request.GET.get('numbers')
    special_chars = request.GET.get('special')

    if uppercase:
            characters.extend(characters_upper)
    if numbers:
        characters.extend(nums)  
    if special_chars:
        characters.extend(specials)

    for _ in range(lenght) :
        thepassword += random.choice(characters)


    return render(request, 'generator/password.html', {'password': thepassword})