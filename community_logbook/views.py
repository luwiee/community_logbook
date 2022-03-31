import json
from datetime import datetime

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from accounts.models import homeOwner
from django.contrib.auth.hashers import check_password

from logging_app.models import log


def index(request):
    if request.user.is_staff:
        return logs(request)
    if request.user.is_authenticated:
        return profile(request)
    return render(request, 'index.html')


@login_required
def profile(request):
    is_staff = request.user.is_staff
    # Use is_staff in the future when home_owner code is finished

    my_user = request.user
    home_owner = homeOwner.objects.get(user=my_user)
    fam_code = home_owner.family_code
    house_code = home_owner.house.housing_lot
    context = {
        'acc_type': 'HOMEOWNER',
        'fam_code': fam_code,
        'house_code': house_code,
    }
    return render(request, 'profile.html', context)


@login_required
def logs(request):
    if not request.user.is_staff:
        home_owner = homeOwner.objects.get(user=request.user)
        logs_var = log.objects.filter(user=home_owner, is_logged=True)
    else:
        logs_var = log.objects.filter(is_logged=True)

    context = {
        "logs": logs_var,
    }
    return render(request, 'logs.html', context)


def qr_gen_page(request):
    return render(request, 'qr-generate.html')

@login_required
def qr_scan_page(request):
    return render(request, 'qr-scan.html')

# End-point for accepting a log_entry with qr id as input
class AcceptLogEntry(LoginRequiredMixin, View):
    login_url = '/'

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        if request.method == 'POST':
            id = request.POST['id']
            my_log = log.objects.get(id=id)
            print(id, my_log)
            if not my_log.is_logged:
                my_log.staff = request.user
                my_log.time_stamp = datetime.now()
                my_log.is_logged = True
                my_log.save()
                print(my_log.time_stamp)
            data = {
                "id": my_log.id,
                "type": my_log.type,
                "name": my_log.user.family_code if my_log.user is not None else my_log.visitor_name,
                "destination": my_log.destination,
                "timestamp": str(my_log.time_stamp),
                "staff": str(my_log.staff),
            }
            return HttpResponse(json.dumps(data))

# End-point for generating a log_entry with qr return as id
class GenerateLogEntry(View):
    login_url = '/'

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        if request.method == 'POST':
            type_v = request.POST['type']
            destination = request.POST['destination']
            if request.user.is_authenticated:
                home_owner = homeOwner.objects.get(user=request.user)
                old_logs = log.objects.filter(user=home_owner, is_logged=False)
                for log_v in old_logs:
                    log_v.delete()
            else:
                old_logs = log.objects.filter(user=None, is_logged=False)
                for log_v in old_logs:
                    log_v.delete()
            # get all unfinished logs

            my_log = log.objects.create(type=type_v, destination=destination)
            if request.user.is_authenticated:
                my_log.user = home_owner
                my_log.save()
            else:
                my_log.visitor_name = request.POST['visitor_name']
                my_log.save()

            qr_html = render_to_string('qr_template.html', {"code": my_log.id})
            return HttpResponse(json.dumps(qr_html))


# End-point for updating password
class UpdatePassword(LoginRequiredMixin, View):
    login_url = '/'

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        if request.method == 'POST':
            user = request.user
            real_current_password = user.password
            new_password = request.POST['new_password']
            current_password = request.POST['current_password']
            check = check_password(current_password, real_current_password)
            user.set_password(new_password)

            user.save()
            update_session_auth_hash(request, request.user)
            if check:
                return HttpResponse(json.dumps("Password changed successfully!"))
            return HttpResponse(json.dumps("Current password is invalid!"))
