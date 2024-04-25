from rest_framework import serializers
from .models import Career,Application

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        