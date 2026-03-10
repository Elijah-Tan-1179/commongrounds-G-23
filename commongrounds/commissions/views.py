from django.shortcuts import render, get_object_or_404
from .models import Commission

# List view for commission model
def commission_list(request):

    commissions = Commission.objects.all()

    context = {
        "commissions": commissions,
    }

    return render(
        request,
        "commissions/commission_list.html",
        context,
    )

# Detail view for commission model
def commission_detail(request, pk):

    commission = get_object_or_404(
        Commission,
        pk=pk,
    )

    context = {
        "commission": commission,
    }

    return render(
        request,
        "commissions/commission_detail.html",
        context,
    )