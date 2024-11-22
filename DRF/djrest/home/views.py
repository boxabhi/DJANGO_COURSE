from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import *


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
    serializer = StudentSerializer(data = data)
    if not serializer.is_valid():
        return Response({
            "status" : False,
            "message" : "record not created",
            "errors" : serializer.errors
        })
    serializer.save()
    
    return Response({
        "status" : True,
        "message" : "record created",
        "data" : serializer.data
    })  


@api_view(['PATCH'])
def update_record(request):
    
    data = request.data
    if data.get('id') is None:
        return Response({
            "status" : False,
            "message" : "record not created",
            "errors" : "id is required"
        })
    student_obj = Student.objects.get(id = data.get('id'))
    serializer = StudentSerializer(student_obj, data = data, partial = True)
    if not serializer.is_valid():
        return Response({
            "status" : False,
            "message" : "record not updated",
            "errors" : serializer.errors
        })
    serializer.save()
    
    return Response({
        "status" : True,
        "message" : "record updated",
        "data" : serializer.data
    }) 

@api_view(['GET'])
def get_records(request):
    if request.GET.get('id'):
        student = Student.objects.get(id = request.GET.get('id'))
        serializer = StudentSerializer(student)
        return Response({
        "status" : True,
        "message" : "record fetched",
        "data" : serializer.data
    })  

    queryset = Student.objects.all()
    serializer = StudentSerializer(queryset, many =True)
    return Response({
        "status" : True,
        "message" : "record fetched",
        "data" : serializer.data
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