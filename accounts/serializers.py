from rest_framework import serializers
from django.contrib.auth.models import User

from accounts.models import EmployeeInfo

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


#Employee Status
class EmployeeInfoSerializer(serializers.ModelSerializer):
    # total_duration = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeInfo
        fields = ('id', 'employee', 'login_time', 'logout_time','login_count', 'logout_count','attendance_status','created_date')