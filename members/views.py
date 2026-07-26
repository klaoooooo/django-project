from django.shortcuts import render
from .models import Member

def index(request):
    members = Member.objects.all()
    query = request.GET.get('q', '')
    if query:
        members = members.filter(
            firstName__icontains=query
        ) | members.filter(
            lastName__icontains=query
        ) | members.filter(
            id__icontains=query
        ) | members.filter(
            country__icontains=query
        )
    return render(request, 'index.html', {
        'members': members,
        'query': query,
        'total': members.count()
    })

def profile(request, id):
    member = Member.objects.get(id=id)
    return render(request, 'profile.html', {'member': member})