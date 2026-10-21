from django.shortcuts import render
from django.contrib import messages
from doctor.forms import doctorForm
from django.http import HttpResponse
from doctor.models import doctorModel
from users.models import UserRegistrationModel


# Create your views here.

def doctorLogin(request):
    return render(request, 'doctorlogin.html', {})


def doctorregistrationaction(request):
    if request.method == 'POST':
        form = doctorForm(request.POST)
        if form.is_valid():
            form.save()
            print("succesfully saved the data")
            return render(request, 'doctorlogin.html')

        else:
            print("form not valied")
            return HttpResponse("form not valied")
    else:
        form = doctorForm()
        return render(request, "doctorregister.html", {"form": form})


def doctorlogincheck(request):
    if request.method == 'POST':
        sname = request.POST.get('email')
        print(sname)
        spasswd = request.POST.get('upasswd')
        print(spasswd)
        try:
            check = doctorModel.objects.get(email=sname, passwd=spasswd)
            # print('usid',usid,'pswd',pswd)
            print(check)
            request.session['name'] = check.name
            print("name", check.name)
            status = check.status
            print('status', status)
            if status == "Activated":
                request.session['email'] = check.email
                return render(request, 'doctor/doctorhomepage.html')
            else:
                messages.success(request, 'doctor is not activated')
                return render(request, 'doctorlogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid name and password')
        return render(request, 'doctorlogin.html')


def doctorlogout(request):
    return render(request, 'doctorlogin.html', {})


def paitentdetails(request):
    data = UserRegistrationModel.objects.all()
    return render(request, 'doctor/paitentdetails.html', {'data': data})