from rest_framework import serializers
from home.models import Event,Booking,Ticket
from django.contrib.auth.models import User
import sys, os

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['event'] = EventSerializer(instance.ticket.event).data
        response['ticket'] = TicketSerializer(instance.ticket).data
        
        return response

class TicketBookingSerializer(serializers.Serializer):
    event = serializers.IntegerField()
    ticket_type = serializers.CharField()
    total_person = serializers.IntegerField()
    user = serializers.IntegerField()

    def validate_event(self, value):
        if not Event.objects.filter(id=value, status="Happening").exists():
            raise serializers.ValidationError("Event does not exist")
        return value

    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("User does not exist")
        return value
    

    def validate(self, data):
        event = Event.objects.get(id=data['event'])
        total_person = event.capacity
        if total_person > 3:
            raise serializers.ValidationError("You can only book 3 tickets")

        return data





    def create(self , validated_data):
        try:
            event = Event.objects.get(id=validated_data['event'])
            user = User.objects.get(id=validated_data['user'])
            total_person = validated_data['total_person']
            ticket_type = validated_data['ticket_type']

            print(event, ticket_type, total_person, user)
            ticket = Ticket.objects.create(   
                event = event,
                ticket_type = ticket_type,
                total_person= int(total_person))

            total_price = event.ticket_price * total_person

            booking = Booking.objects.create(
                ticket = ticket,
                user =user,
                status = "Paid",
                total_price = total_price
            )

            return {
                "event" : event.id,
                "ticket_type" : ticket_type,
                "total_person" : total_person,
                "user" : user.id,
            }
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(e,exc_type, fname, exc_tb.tb_lineno)