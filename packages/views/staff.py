from packages.models import Partner
from django.shortcuts import render
from util import is_member

def staff_view(request):
    if not is_member(request.user, 'staff'):
        return render(request, 'errors/access_restricted.html', {})

    context = {
        'partners': Partner.objects.all(),
        'is_staff': True
    }

    return render(request, 'packages/staff.html', context)