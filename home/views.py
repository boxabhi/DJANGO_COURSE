from django.shortcuts import render,redirect
from django.http import HttpResponse
from home.forms import StudentForm
from home.models import Sudent2


def index(request):
    context = {'form' : StudentForm}
    if request.method == "POST":

        name = request.POST.get('full_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        upload_file = request.FILES['upload_file']

        Sudent2.objects.create(
           name = name,
            age = age,
            gender = gender,
            upload_file  = upload_file,
        )

        print(name , age , gender)

        return redirect("/thank-you/")



    return render(request , 'index.html', context)


def contact(request):
    return render(request , 'contact.html')


def about(request):
    return render(request , 'about.html')

def dynamic_route(request, number):
    return HttpResponse(f"Response by Dynamic route you entered {number}")


def thank_you(request):
    return HttpResponse("Thank you your response is recorded")