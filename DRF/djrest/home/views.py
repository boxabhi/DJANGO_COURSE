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
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from utils.paginate import (
    LargeResultPagination,StandardResultsSetPagination,CustomCursorPagination)


from django.shortcuts import render, redirect



class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status" :True,
                "message" : "user registered succesfully",
                "data" : {}
            })
        return Response({
                "status" :False,
                "message" : "keys missing",
                "data" : serializer.errors
                
            })


class LoginAPI(APIView):
    def post(self , request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username = serializer.data['username'],
                password = serializer.data['password'])
            if user is None:
                return Response({
                     "status" :False,
                    "message" : "invalid credentials",
                    "data" : {}
            }, status = 401)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "status" :True,
                "message" : "user token",
                "data" : {
                    "token" : token.key
                }
            })
        return Response({
                "status" :False,
                "message" : "keys missing",
                "data" : serializer.errors
                
            })


from .permissions import IsProductOwnerPermission,IsVipUser
from rest_framework.throttling import UserRateThrottle
from utils.throttle import CustomThrottle
from rest_framework.throttling import ScopedRateThrottle
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer    
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsProductOwnerPermission,IsVipUser]
    pagination_class = CustomCursorPagination
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'product'

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def list(self, request, *args, **kwargs):
        print(request.user)
        return super().list(request, *args, **kwargs)



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
    

from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly

SAFMETHOD = ["GET", "HEAD", "OPTIONS"]

class StudentAPI(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
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


from django.core.paginator import Paginator
from utils.paginate import paginate

class AuthorAPI(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'product'
    def get(self , request):
        authors = Author.objects.all()
        pagenumber = request.GET.get('page', 1)
        paginator = Paginator(authors, 10)
        data = paginate(authors, paginator, pagenumber)
        serializer = AuthorSerializer(data['results'] , many =True)
        data['results'] = serializer.data
        return Response(data)
    
import csv

def index(request):
    context = {
        'uploaded_files' : File.objects.filter(user = request.user),
        'uploaded_data' : Person.objects.filter(user = request.user),
        'button_to_show' : not DeleteRequest.objects.filter(
            user = request.user , is_done = False).count() and
            Person.objects.filter(user = request.user).count()
    }


    return render(request,'index.html', context)

def upload_file(request):
    file = request.FILES['file']
    if file.name.endswith('.csv'):
        file_obj = File.objects.create(
            user = request.user,
            file = file
        )
        with open(file_obj.file.path, mode='r') as file:
            csv_reader = csv.reader(file)
            index = 1
            
            for lines in csv_reader:
                if index == 1:
                    index += 1
                    continue
                name = lines[0]
                age = lines[1]
                email = lines[2]
                Person.objects.create(
                    name = name,
                    age = age,
                    email = email,
                    user = request.user
                )

            

    return redirect('/')


def delete_request(request):
    DeleteRequest.objects.create(
        user = request.user
    )
    return redirect('/')

# class FileAPI(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes  = [TokenAuthentication]

#     def post(self , request):
#         data = request.data
#         data['user'] = request.user.id
#         serializer = FileSerializer(data = data)
#         if not serializer.is_valid():
#             return Response({
#                 "status" : False,
#                 "data" : serializer.errors
#             })
#         serializer.save()
#         return Response({'status' : True,
#                          'message' : "file uploaded"})


