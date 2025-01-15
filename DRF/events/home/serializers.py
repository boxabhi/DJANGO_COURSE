from rest_framework import serializers
from .models import User, Event, Category,Booking



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    



class EventSerializer(serializers.ModelSerializer):
    event_slug = serializers.SlugField(required =False,allow_null=True, allow_blank = True)
    class Meta:
        model = Event
        fields = '__all__'


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = {
            'id' : instance.category.id,
            'category_name' : instance.category.category_name
        }
        return data


