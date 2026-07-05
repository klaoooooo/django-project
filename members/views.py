import csv
import os
from django.shortcuts import render

def index(request):
    members = []
    csv_path = os.path.join(os.path.dirname(__file__), 'Athlests.member.csv')
    
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            initials = (row['firstName'][0] + row['lastName'][0]).upper()
            row['initials'] = initials
            members.append(row)  
    
    query = request.GET.get('q', '')
    if query:
        members = [m for m in members if 
            query.lower() in m['firstName'].lower() or
            query.lower() in m['lastName'].lower() or
            query.lower() in m['id'].lower() or
            query.lower() in m['country'].lower()]
    
    return render(request, 'index.html', {
        'members': members,  
        'query': query,
        'total': len(members)
    })

def profile(request, id): 
    csv_path = os.path.join(os.path.dirname(__file__), 'Athlests.member.csv')
    member = None
    
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['id'] == id:
                row['initials'] = (row['firstName'][0] + row['lastName'][0]).upper()
                member = row
                break
    
    return render(request, 'profile.html', {'member': member})