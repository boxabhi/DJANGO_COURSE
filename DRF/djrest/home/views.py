from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import *
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    

    @action(detail=False, methods=['POST'])
    def export_product(self , request):
        return Response({
            "status" : True,
            "message" : "file exported",
            "data" : {}
        })

    @action(detail=True, methods=['POST'])
    def send_email_product(self , request, pk):
        print("Email sent!!!", pk)
        return Response({
            "status" : True,
            "message" : f"email sent {pk}",
            "data" : {}
        })
    

    


    




class ProductListCreate(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class StudentModelListView(ListModelMixin,CreateModelMixin,DestroyModelMixin, GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.filter(name__startswith = "r")

    def perform_create(self, serializer):
        return super().perform_create(serializer)

    def get(self, request, *args, **kwargs):
        return self.list(request,*args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        return self.create(request,*args, **kwargs)
    



class StudentAPI(APIView):

    def get(self , request):
        queryset = Student.objects.all().order_by('-name')
        serializer  = StudentSerializer(queryset , many = True)
        return Response({
            "status" : True,
            "message" : "record fetched",
            "data" : serializer.data
        })  
    
    def post(self, request):
        data = request.data
        serializer  = StudentSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status" : False,
                "message" : "record not updated",
                "errors" : serializer.errors
            })
        serializer.save()
        return Response({
            "status" : True,
            "message" : "record created",
            "data" : serializer.data
        }) 





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
        queryset = Student.objects.all().order_by('-name')
        serializer  = StudentSerializer(queryset , many = True)
       
        return Response({
            "status" : True,
            "message" : "record fetched",
            "data" : serializer.data
        })  
    elif request.method == "POST":
        data = request.data
        serializer  = StudentSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status" : False,
                "message" : "record not updated",
                "errors" : serializer.errors
            })
        serializer.save()
        
        return Response({
            "status" : True,
            "message" : "record created",
            "data" : serializer.data
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
    



@api_view(['GET'])
def get_book(request):
    queryset = Book.objects.all()
    serializer = NewBookSeriallizer(queryset, many = True)
    return Response({
        "status" : True,
        "message" : "record fetched",
        "data" : serializer.data
    })  


@api_view(['POST'])
def create_book(request):
    data = request.data
    serializer = NewBookSeriallizer(data = data)
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




@api_view(['POST'])
def create_user(request):
    data = request.data
    serializer = UserSerializer(data = data)
    if not serializer.is_valid():
        return Response({
            "status" : False,
            "message" : "record not created",
            "errors" : serializer.errors
        })
    
    print(serializer.validated_data)
    # serializer.save()
    
    return Response({
        "status" : True,
        "message" : "record created",
        "data" : serializer.data
    })  

