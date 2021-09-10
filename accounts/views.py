import math
import datetime
from django.utils import dateparse

from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

from django.core.exceptions import ValidationError
from django.db.models import Q


from django.contrib.auth import login

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

# from django.core.cache import cache

from rest_framework.views import APIView


from accounts.models import EmployeeAccount, EmployeeInfo
from accounts.serializers import EmployeeInfoSerializer
from accounts.utils import CustomMessage

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


#use of cache to store the login count
# def dashboard(self, request):
#     if request.user.is_authenticated():
#         ct = cache.get('count', version=user.pk)
#         return render(request, 'dashboard.html', {'ct':ct})
#     else:
#         return HttpResponseRedirect('/login/'))


class EmployeeInfoAPI(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            try:
                EmployeeAccount.objects.get(Q(id=request.user.id))
            except EmployeeInfo.DoesNotExist:
                raise CustomMessage("Employee ID is invalid")
            employee_data_obj = EmployeeInfo.objects.filter(Q(employee=request.user) &
                                                          Q(created_date=datetime.datetime.today()))
            serializer_data = EmployeeInfoSerializer(employee_data_obj, many=True).data
            login_count = 0
            logout_count = 0
            for i in serializer_data:
                if i["login_datetime"]:
                    login_count += 1
                if i["logout_datetime"]:
                    logout_count += 1

            # messages.set_level(request, messages.INFO)

            # check Logout request
            if request.POST['action'] == 'logout':
                return redirect('login:login')

            # Login new record times 
            elif request.POST['action'] == 'login':
                try:
                    # Process time
                    # if the user selected login and logout times
                    if request.POST['login'] and request.POST['logout']:
                        # convert login and logout times to time difference in hours and minutes
                        current_date = datetime.date.today()
                        in_start = datetime.datetime.combine(current_date, dateparse.parse_time(request.POST['login']))
                        in_end = datetime.datetime.combine(current_date, dateparse.parse_time(request.POST['logout']))
                        t = in_end - in_start
                        in_hours = math.floor(t.seconds/3600)
                        tot_minutes = (t.seconds % 3600)/60
                        quarters = math.floor(tot_minutes/15)
                        in_minutes = quarters * 15
                        # defines max number of hours that can be worked for a single day and login condition
                        if int(in_hours) > 10:
                            messages.warning(request, 'The max number of working hours are 10.')
                            return Response({"data": {'message': 'Employee is absent'}},status=status.HTTP_200_OK)
                    # if the user selected hours and minutes duration
                    else:
                        in_hours = request.POST['hours']
                        in_minutes = request.POST['minutes']
                except KeyError:
                    return "Key does not exist" # Any of the inputs are not available for some reason

                else:
                    # Creates new entry for time record
                    selected_user = EmployeeAccount.objects.get(Username=request.user)
                    selected_user.workhour_set.create(Employee=selected_user.pk, hours=in_hours, minutes=in_minutes)
                    selected_user.save()
                    messages.success(request, 'Employee time successfully updated!')

            return Response({"data": {"is_success": True, 'message': serializer_data, "login_count": login_count,
                                      "logout_count": logout_count, "hours": in_hours, "minutes": in_minutes}},
                            status=status.HTTP_200_OK)
        except CustomMessage as e:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except (ParseError, ZeroDivisionError, MultiValueDictKeyError, KeyError, ValueError, ValidationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "fail", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)