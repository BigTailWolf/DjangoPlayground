from django.shortcuts import render, redirect
from django.http import JsonResponse
from random import choice

# Create your views here.
def index(request):
    if 'next' not in request.session:
        init(request)

    return render(request, 'index.html')


def end(rquest):
    return redirect('/')


def reset(request):
    request.session.flush()
    init(request)
    return redirect('/')


def init(request):
    request.session['ai_choice'] = choice(('rock', 'paper', 'scissors'))
    request.session['rock'] = [0, 0, 0]
    request.session['paper'] = [0, 0, 0]
    request.session['scissors'] = [0, 0, 0]
    request.session['win'] = 0
    request.session['tie'] = 0
    request.session['loss'] = 0


def process(request, option):
    print(request.session.items())
    if 'user_last' in request.session:
        last = request.session['user_last'] #

        # Update learning model
        if option == 'rock':     request.session[last][0] += 1
        if option == 'paper':    request.session[last][1] += 1
        if option == 'scissors': request.session[last][2] += 1

    request.session['user_last'] = option # Update user last choice info

    ai_choice = request.session['ai_choice']
    # Predict for the next round
    idx = (request.session[option].index(max(request.session[option])) + 1) % 3
    request.session['ai_choice'] = ('rock', 'paper', 'scissors')[idx]

    # Settlement of this round
    result = check(option, ai_choice)
    request.session[result] += 1

    return JsonResponse({
        'result': result,
        'ai_choice': ai_choice,
        'win': request.session['win'],
        'tie': request.session['tie'],
        'loss': request.session['loss'],
    })


def check(user_choice, ai_choice):
    return {
        'rock':     {'rock': 'tie',  'paper':'loss', 'scissors':'win' },
        'paper':    {'rock': 'win',  'paper':'tie',  'scissors':'loss'},
        'scissors': {'rock': 'loss', 'paper':'win',  'scissors':'tie' },
    }[user_choice][ai_choice]
