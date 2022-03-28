from django.shortcuts import render
from django.http import HttpResponse
import random
import requests
import hashlib

import generator

curr_password = []
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
    curr_password.append(thepassword)

    return render(request, 'generator/password.html', {'password': thepassword})

def request_api_data(query_char):
    url = f'https://api.pwnedpasswords.com/range/{query_char}'

    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code} ')
    return res


def get_pas_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def check_if_pwned(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)

    return get_pas_leaks_count(response, tail)


def password_validation(request):
    if len(curr_password) > 0:
        pwd = curr_password[-1]

        count = check_if_pwned(pwd)
        if count:
            print(f'{pwd} was found {count}, You should probably change your password')
            return render(request, 'generator/password_validation.html', {'password': pwd, 'pwned': True, 'count': count})
        else:
            return render(request, 'generator/password_validation.html', {'password': pwd, 'pwned' : False, 'count': count})