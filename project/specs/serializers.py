from rest_framework import serializers
from .models import *

class PhoneNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneName
        fields = '__all__'
        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
