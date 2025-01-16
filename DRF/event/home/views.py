from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (TicketBookingSerializer,
    Event, EventSerializer,RegisterSerializer, LoginSerializer, Booking, BookingSerializer)
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from .permission import IsAdminUser
from rest_framework.decorators import action

from rest_framework.exceptions import MethodNotAllowed
from django.db.models import Q

#username
#password
#email


class ResgiserAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message" : "Account created",
                "data" : {}
            })
        return Response({
            "status": False,
                "message" :"Account not created",
                "data" : serializer.errors
        })
        return Response('Hello')

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            user = authenticate(
                username = serializer.validated_data['username'],
                password = serializer.validated_data['password']
            )

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "status": True,
                    "message" : "Login successful",
                    "data" : {"token": token.key}
                })
            else:
                return Response({
                    "status": False,
                    "message" : "invalid credentials",
                    "data" : {}
                })
        return Response({
            "status": False,
                "message" :"Login failed",
                "data" : serializer.errors
        })

class PublicEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get']


    @action(detail=False, methods=['GET'])
    def search_events(self , request):
        search = request.GET.get('search')
        events = Event.objects.all()
        if search:
            events = events.filter(
            Q(title__icontains=search) | Q(description__icontains=search))
        
        serializer = EventSerializer(events, many=True)
        return Response({
            "status" : True,
            "message" : "Events fetched",
            "data" : serializer.data
        })



class PrivateEventViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
  

    @action(detail=False, methods=['GET'])
    def get_bookings(self , request):
        bookings = Booking.objects.filter(user = request.user)


        serializer = BookingSerializer(bookings, many=True)
        return Response({
            "status" : True,
            "message" : "Bookings fetched",
            "data" : serializer.data
        })


    @action(detail=False, methods=['POST'])
    def create_booking(self , request):
        data = request.data
        serializer = TicketBookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status" : True,
                "message" : "Booking created",
                "data" : serializer.data
            })


        return Response({
            "status" : False,
            "message" : "Booking not created",
            "data" : serializer.errors
        })