from .models import *
from rest_framework import serializers

class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields = ['id', 'advisor_name', 'advisor_photo_url']

class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class BookingSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = ['date_time']

class ShowBookingSerializer(serializers.ModelSerializer):
    advisor = AdvisorSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['advisor', 'date_time', 'id']

