import csv
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from members.models import Member

with open('myproject/Athlests.member.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Member.objects.get_or_create(
            id=row['id'],
            defaults={
                'country': row['country'],
                'firstName': row['firstName'],
                'lastName': row['lastName'],
                'gender': row['gender'],
                'dateOfBirth': row['dateOfBirth'],
                'classification': row['classification'],
                'email': row['email'],
            }
        )
print("Done!")