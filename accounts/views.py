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

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated

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

    def get(self, request):
        login_count = 0
        logout_count = 0
        employee_data_obj = EmployeeInfo.objects.filter(Q(employee=request.user) &
                                                        Q(created_date=datetime.datetime.today()))
        working_time = (employee_data_obj.end_datetime - employee_data_obj.start_datetime)
        serializer_data = EmployeeInfoSerializer(employee_data_obj, many=True).data
        current_date = datetime.date.today()
        in_start = datetime.datetime.combine(current_date, dateparse.parse_time(request.data['login_time']))
        in_end = datetime.datetime.combine(current_date, dateparse.parse_time(request.data['logout_time']))
        t = in_end - in_start
        in_hours = math.floor(t.seconds/3600)
        tot_minutes = (t.seconds % 3600)/60
        quarters = math.floor(tot_minutes/15)
        in_minutes = quarters * 15
        # defines max number of hours that can be worked for a single day and login condition
        if in_hours > working_time:
            attendance_status = "Present"
        else:
            attendance_status = "Absent"
        
        # Creates new entry for time record
        selected_user = EmployeeInfo.objects.get(Employee=request.user)
        selected_user.workhour_set.create(Employee=selected_user.pk, hours=in_hours, minutes=in_minutes)
        selected_user.save()

        return Response({"data": {"is_success": True, 'message': serializer_data, "login_count": login_count,
                                    "logout_count": logout_count, "hours": in_hours, "minutes": in_minutes, 'attendance_status':attendance_status}},
                        status=status.HTTP_200_OK)


# def logged(request):
#   logged_users = LoggedUser.objects.all().order_by('username')
#   return Response({'logged_users': logged_users},
#                             context_instance=RequestContext(request))
