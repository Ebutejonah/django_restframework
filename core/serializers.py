from rest_framework import serializers
from .models import Student, Advocate


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'username',
            'age'
        )

class AdvocateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advocate
        fields = '__all__'