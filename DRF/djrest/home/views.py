from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student


@api_view(['GET', 'POST', 'PATCH','PUT', 'DELETE'])
def index(request):
    print(request.method)
    students = ["Abhijeet", "Nitesh", "Pritam"]
    data = {
        "status" : True,
        "message" : "This is from django rest framework",
        "students" : students,
        "method" : f"You called this API with {request.method}"
    }
    return Response(data)

@api_view(['GET', 'POST', 'PATCH','PUT', 'DELETE'])
def student(request):
    if request.method == "GET":
        students = [
        {
            "id": student.id,
            "name": student.name,
            "dob": student.dob,
            "email": student.email,
            "phone_number": student.phone_number,
        }
            for student in Student.objects.all().order_by('-name')
        ]
        return Response({
            "status" : True,
            "message" : "record created",
            "data" : students
        })  
    elif request.method == "POST":
        data = request.data
        Student.objects.create(**data)
        return Response({
            "status" : True,
            "message" : "record created"
        })  
    elif request.method == "DELETE":
        try:
            data = request.data
            student = Student.objects.get(id = data.get('id')).delete()
            return Response({
                "status" : True,
                "message" : "record deleted",
                "data" : {}
            })  
        except Exception as e:
            return Response({
                "status" : False,
                "message" : "invalid id",
                "data" : {}
            })   
            
    else:
        return Response({
                "status" : False,
                "message" : "invalid method",
                "data" : {}
            })    

@api_view(['POST'])
def create_record(request):
    data = request.data
    Student.objects.create(**data)
    return Response({
        "status" : True,
        "message" : "record created"
    })  

@api_view(['GET'])
def get_records(request):
    students = [
        {
            "id": student.id,
            "name": student.name,
            "dob": student.dob,
            "email": student.email,
            "phone_number": student.phone_number,
        }
        for student in Student.objects.all().order_by('-name')
    ]
    return Response({
        "status" : True,
        "message" : "record created",
        "data" : students
    })  

@api_view(['DELETE'])
def delete_record(request):
    try:
        data = request.data
        student = Student.objects.get(id = data.get('id')).delete()
        return Response({
            "status" : True,
            "message" : "record deleted",
            "data" : {}
        })  
    except Exception as e:
        return Response({
            "status" : False,
            "message" : "invalid id",
            "data" : {}
        })  