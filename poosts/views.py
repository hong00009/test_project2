from django.shortcuts import render, redirect

from .models import Poost

def index(request):
    poosts = Poost.objects.all()

    context = {
        'poosts' : poosts,
    }
    return render(request, 'poosts/index.html', context)

def detail(request, id):
    poost = Poost.objects.get(id=id)

    context = {
        'poost' : poost,
    }
    return render(request, 'poosts/detail.html', context)

def new(request):
    return render(request, 'poosts/new.html')

def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')

    poost = Poost()
    poost.title = title
    poost.content = content
    poost.save()

    return redirect('poosts:detail', id=poost.id)

def delete(request, id):
    poost = Poost.objects.get(id=id)
    poost.delete()
    
    return redirect('poosts:index')

def edit(request, id):
    poost = Poost.objects.get(id=id)

    context = {
        'poost' : poost
    }
    return render(request, 'poosts/edit.html', context)

def update(request, id):
    poost = Poost.objects.get(id=id)

    title = request.POST.get('title')
    content = request.POST.get('content')

    poost.title = title
    poost.content = content
    poost.save()

    return redirect('poosts:detail', id=poost.id)