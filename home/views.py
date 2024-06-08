from django.shortcuts import render,redirect
from django.http import HttpResponse
from home.forms import StudentForm
from home.models import Sudent2, Student
from django.db.models import Q


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



def search_page(request):
    students = Student.objects.all()

    search = request.GET.get('search')
    age = request.GET.get('age')
    age = request.GET.get('age')
    score = request.GET.get('')
    if search:
        students = students.filter(
            Q(name__icontains = search) |
             Q(mobile_number__icontains = search) |
             Q(email__icontains = search) |
             Q(gender__icontains = search) |
             Q(student_bio__icontains = search))



    if age:
        print(age, type(age))
        if age == "1":
            students = students.filter(age__gte = 18 , age__lte = 20).order_by('age')
        if age == "2":
            students = students.filter(age__gte = 20 , age__lte = 22).order_by('age')

        if age == "3":
            students = students.filter(age__gte = 22 , age__lte = 24).order_by('age')


    context = {'students' : students, 'search' : search}
    return render(request, 'search.html', context)