from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from util import user_partners

@staff_member_required
def partners_view(request):
    return render(request, 'packages/partners.html', {'partners': user_partners(request.user)})