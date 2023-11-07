from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from admin_p.models import TableModel


def user_is_waiter(user):
    return user.groups.filter(name='Waiters').exists()


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(user_is_waiter, login_url='/'), name='dispatch')
class WaiterPanel(View):
    def get(self, request):
        tables = TableModel.objects.all()
        data = {'tables':tables}
        return render(request, 'waiter/WaiterPanel.html', data)


