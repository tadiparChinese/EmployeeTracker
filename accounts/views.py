import math
import datetime
from django.utils import dateparse

from django.contrib import messages

from django.shortcuts import redirect

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.template import RequestContext


from django.contrib.auth import login
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView

# from django.core.cache import cache

from rest_framework.views import APIView


from accounts.models import EmployeeAccount, EmployeeInfo
from accounts.serializers import EmployeeInfoSerializer
from accounts.utils import CustomMessage

#User API
class UserAPIView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user




# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 




class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


#Logout view is handled by knox



class EmployeeInfoAPI(APIView):
    permission_classes = (IsAuthenticated, )
    # serializer_class = EmployeeInfoSerializer

    def get(self, request):
        login_count = 0
        logout_count = 0
        employee_data_obj = EmployeeInfo.objects.filter(Q(employee=request.user) &
                                                        Q(created_date=datetime.datetime.today()))
                                                
        # starting from 9AM to 5PM
        fixed_login_time = datetime.now().strftime("%Y-%m-%d")  + " 09:00"
        fixed_logout_time = datetime.now().strftime("%Y-%m-%d")  + " 17:00"
        working_time = EmployeeInfo.objects.filter(date__range= (fixed_login_time, fixed_logout_time))
        # working_time = (employee_data_obj.end_datetime - employee_data_obj.start_datetime)
        login_time = working_time.first()
        logout_time = working_time.last()
        serializer_data = EmployeeInfoSerializer(employee_data_obj, many=True).data
        current_date = datetime.date.today()
        # for each employee_data_obj creation increase the counter
        for emp in employee_data_obj:
            if emp.login_time and emp.logout_time:
                in_start = datetime.datetime.combine(current_date, dateparse.parse_time(request.data(login_time)))
                in_end = datetime.datetime.combine(current_date, dateparse.parse_time(request.data(logout_time)))
                t = in_end - in_start # actual working window
                in_hours = math.floor(t.seconds/3600)
                tot_minutes = (t.seconds % 3600)/60
                quarters = math.floor(tot_minutes/15)
                in_minutes = quarters * 15
                login_count+=1
                logout_count+=1
        # defines max number of hours that can be worked for a single day and login condition
        if in_hours >= working_time:
            attendance_status = "Present"
        else:
            attendance_status = "Absent"
        
        # Creates new entry for every time record
        # employee_data_obj = EmployeeInfo.objects.get(Employee=request.user)
        # employee_data_obj.workhour_set.create(Employee=employee_data_obj.pk, hours=in_hours, minutes=in_minutes)
        serializer_data.save()

        return Response({"data": {"is_success": True, 'message': serializer_data, "fixed_logout_time": fixed_logout_time, "fixed_login_time":fixed_login_time, "login_count": login_count,
                                    "logout_count": logout_count, 'attendance_status':attendance_status}},
                        status=status.HTTP_200_OK)
