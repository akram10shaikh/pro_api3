# views.py
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from myapp.models import *
from myapp.serializers import *
from django.shortcuts import render
import pyrebase
import random
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.views import View
import io
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from myapp.models import *
from rest_framework.renderers import JSONRenderer

from pyfcm import FCMNotification

from firebase_admin import messaging
from firebase_admin import firestore


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import os
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import render
from django.http import Http404
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

def get_json_file(file_path):
    """Helper function to return the content of a JSON file."""
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if not os.path.exists(full_path):
        raise Http404("File not found.")

    with open(full_path, 'r') as file:
        data = json.load(file)

    return data


@require_GET
def terms_and_conditions(request):
    try:
        data = get_json_file('json/termsAndConditions.json')
        return JsonResponse(data)
    except Http404:
        return JsonResponse({"error": "File not found"}, status=404)


@require_GET
def privacy_policy(request):
    try:
        data = get_json_file('json/privacy.json')
        return JsonResponse(data)
    except Http404:
        return JsonResponse({"error": "File not found"}, status=404)


@require_GET
def faq(request):
    try:
        data = get_json_file('json/faq.json')
        return JsonResponse(data)
    except Http404:
        return JsonResponse({"error": "File not found"}, status=404)




def index(request):
    return render(request,'index.html')


class MyRestaurantNameAPIView(ListCreateAPIView):
    queryset = RestaurantName.objects.all()
    serializer_class = MyRestaurantNameSerializer

class MyRestaurantNameAPIView1(RetrieveUpdateDestroyAPIView):
    queryset = RestaurantName.objects.all()
    serializer_class = MyRestaurantNameSerializer

class MyTicket_raiseAPIView(ListCreateAPIView):
    queryset = Ticket_raise.objects.all()
    serializer_class = MyTicket_raiseSerializer


class MyTicket_raiseAPIView1(RetrieveUpdateDestroyAPIView):
    queryset = Ticket_raise.objects.all()
    serializer_class = MyTicket_raiseSerializer


class MyOrderAPIView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "order_status_updates",
            {
                "type": "new",
                'id': order.id,
                'user': order.user.id if order.user else None,
                'restaurant': order.resturant.id if order.resturant else None,
                'customer_name': order.customer_name,
                'bill_id': order.bill_id,
                'order_date': order.order_date.isoformat() if order.order_date else None,
                'delivery_data': order.delivery_data.isoformat() if order.delivery_data else None,
                'amount': order.amount,
                'note': order.note,
                'tag': order.tag,
                'order_status': order.order_status,
                'restaurant_name':order.resturant.restaurant_name,
                'address':order.address,
            }
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyOrderAPIView1(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = MyOrderSerializer

    def perform_update(self, serializer):
        order = serializer.save()
        channel_layer = get_channel_layer()
        tokendata = FCMDevice.objects.get(user=order.user.id)
        token = tokendata.fcm_token

        if str(order.order_status).lower() != 'ongoing':
            if str(order.order_status).lower() == 'completed':
                msg = "order completed"

            if str(order.order_status).lower() == 'order ready':
                msg = "order ready"
        else:
            msg = "order Ongoing"


        message = messaging.Message(
                notification=messaging.Notification(
                    title="Order Status",
                    body=msg,
                ),
                token = token
            )
        messaging.send(message)

        async_to_sync(channel_layer.group_send)(
            "order_status_updates",
            {
                "type":"updated",
                'id': order.id,
                'user': order.user.id if order.user else None,
                'restaurant': order.resturant.id if order.resturant else None,
                'customer_name': order.customer_name,
                'bill_id': order.bill_id,
                'order_date': order.order_date.isoformat() if order.order_date else None,
                'delivery_data': order.delivery_data.isoformat() if order.delivery_data else None,
                'amount': order.amount,
                'note': order.note,
                'tag': order.tag,
                'order_status': order.order_status,
            }
        )

class MyCustomeUserAPIView(ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = MyCustomUserSerializer

class MyCustomeUserAPIView1(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = MyCustomUserSerializer

class MyFeedbackAPIView(ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = MyFeedbackSerializer


class MySubscriptionAPIView(ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = MySubscriptionSerializer

# OTP generation
@method_decorator(csrf_exempt, name='dispatch')
class Otp(View):
    def post(self,request,*args,**kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        email = python_data.get('email')
        otp = random.randint(111111,999999)
        if email is not None:
            send_mail(
                'Email Verification OTP',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                )
            msg = {'msg':otp}
            return JsonResponse(msg,safe=False)
        msg = {'msg':'Enter the correct email address'}
        return JsonResponse(msg,safe=False)


# Checking the User data
@method_decorator(csrf_exempt, name='dispatch')
class User_check(View):
    def post(self, request, *args, **kwargs):
        # Parse JSON data
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)

        # Get the email from the parsed data
        email = python_data.get('email')
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                # Return user data as JSON with 200 status code
                user_data = {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "date_of_birth": user.date_of_birth,
                    "gender": user.gender,
                    "phone_number": user.phone_number,
                    "profile_image": user.profile_image,
                    "is_active": user.is_active,
                }
                return JsonResponse(user_data, status=200)
            except CustomUser.DoesNotExist:
                msg = {"msg": "User not found"}
                return JsonResponse(msg, status=404)

        # Get the phone number from the parsed data
        phone_number = python_data.get('phone_number')
        if phone_number:
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
                # Return user data as JSON with 200 status code
                user_data = {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "date_of_birth": user.date_of_birth,
                    "gender": user.gender,
                    "phone_number": user.phone_number,
                    "profile_image": user.profile_image,
                    "is_active": user.is_active,
                }
                return JsonResponse(user_data, status=200)
            except CustomUser.DoesNotExist:
                msg = {"msg": "User not found"}
                return JsonResponse(msg, status=404)

        # If neither email nor phone number is provided or found
        msg = {"msg": "Wrong input"}
        return JsonResponse(msg, status=400)

# Checking the token number from email id
@method_decorator(csrf_exempt, name='dispatch')
class Token_check(View):
    def post(self,request,*args,**kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        email = python_data.get('email')
        user = CustomUser.objects.get(email=email)
        token = Token.objects.get(user=user)
        serializer = SingleVariableSerializer({"token":str(token)})
        return JsonResponse(serializer.data, status=200)


# work
@method_decorator(csrf_exempt, name='dispatch')
class OrderStatus(View):
    def post(self,request,*args,**kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        orderId = python_data.get('id')
        order = Order.objects.get(id=orderId)
        if str(order.order_status).lower() != 'ongoing':
            if str(order.order_status).lower() == 'completed':
                msg = {'order':'completed'}
                return JsonResponse(msg,status=200)

            if str(order.order_status).lower() == 'order ready':
                msg = {'order':'order ready'}
                return JsonResponse(msg,status=200)
        else:
            msg = {'order':'ongoing'}
            return JsonResponse(msg,status=200)


# Firebase Notification check
@method_decorator(csrf_exempt, name='dispatch')
class Order_Notification(View):
    def post(self,request,*args,**kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        orderId = python_data.get('id')
        userId = CustomUser.objects.get(id=python_data['user'])
        order_work = Order.objects.get(id=orderId)
        tokendata = FCMDevice.objects.get(user=userId)
        token = tokendata.fcm_token
        if str(order_work.order_status).lower() != 'ongoing':
            if str(order_work.order_status).lower() == 'completed':
                msg = "order completed"

            if str(order_work.order_status).lower() == 'order ready':
                msg = "order ready"
        else:
            msg = "order Ongoing"

        try:
            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)(
            # "order_status_updates",
            # {
            #     "type":"send_order_status",
            #     "order_id":orderId,
            #     "order_status":msg,
            # }
            # )
            message = messaging.Message(
                notification=messaging.Notification(
                    title="Order Status",
                    body=msg,
                ),
                token = token
            )
            response = messaging.send(message)
            return JsonResponse({"message":"Notification Sent","response":response},status=200)
        except Exception as e:
            return JsonResponse({"Error":str(e)},status=500)


# For checking the firebase is connected or not connected
def check_firebase_connection(request):
    try:
        db = firestore.client()
        collections = db.collections()
        return JsonResponse({"status": "connected"})

    except Exception as e:
        return JsonResponse({"status": "not connected", "error": str(e)})

@method_decorator(csrf_exempt, name='dispatch')
class Order_History(View):
    def post(self,request,*args,**kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        userId = python_data.get('id')
        user = CustomUser.objects.get(id=userId)
        order_data = Order.objects.filter(user=user)
        serializer = MyOrderSerializer(order_data,many=True)
        return JsonResponse(serializer.data,safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class RestaurantOrderHistory(View):
    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        restaurant_id = python_data.get('id')
        try:
            restaurant = RestaurantName.objects.get(id=restaurant_id)
        except RestaurantName.DoesNotExist:
            return JsonResponse({'error': 'Restaurant not found'}, status=404)

        order_data = Order.objects.filter(resturant=restaurant)
        serializer = MyOrderSerializer(order_data, many=True)
        return JsonResponse(serializer.data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class RestaurantCheck(View):
    def post(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        python_data = JSONParser().parse(stream)

        user_id = python_data.get('user')
        if user_id is None:
            return JsonResponse({'error': 'User ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:

            restaurant = RestaurantName.objects.get(user=user_id)
        except RestaurantName.DoesNotExist:
            return JsonResponse({'error': 'Restaurant not found for this user'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MyRestaurantNameSerializer(restaurant)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class DeviceRegistrationAPIView(ListCreateAPIView):
    queryset = FCMDevice.objects.all()
    serializer_class = FCMDeviceSerializer

class DeviceRegistrationAPIView1(RetrieveUpdateDestroyAPIView):
    queryset = FCMDevice.objects.all()
    serializer_class = FCMDeviceSerializer

@method_decorator(csrf_exempt, name='dispatch')
class StartSession(View):
    def post(self, request, *args, **kwargs):
        stream = io.BytesIO(request.body)
        python_data = JSONParser().parse(stream)

        try:
            user = CustomUser.objects.get(id=python_data['id'])
            data =FCMDevice.objects.get(user=user,device=python_data['device'])
            if data:
                data.active = True
                data.save()
                return JsonResponse({"msg":"session is active"})

        except:
            user = CustomUser.objects.get(id=python_data['id'])
            FCMDevice.objects.create(
                device=python_data['device'],
                user = user,
                fcm_token=python_data['fcm_token'],
                platform = python_data['platform'],
                active=python_data['active'],
            )
            return JsonResponse({"msg":"session created"})

@method_decorator(csrf_exempt,name='dispatch')
class LogoutSession(View):
    def post(self,request,*args, **kwargs):
        stream = io.BytesIO(request.body)
        python_data = JSONParser().parse(stream)

        try:
            user = CustomUser.objects.get(id=python_data['id'])

            if python_data['fcm_token'] or user:
                data = FCMDevice.objects.get(user=user,fcm_token=python_data['fcm_token'])
                data.active = False
                data.save()

                token = python_data['fcm_token']
                msg = "logout"
                message = messaging.Message(
                notification=messaging.Notification(
                    title="Session Expired",
                    body=msg,
                ),
                token = token
                )
                response = messaging.send(message)
                return JsonResponse({"msg":"Logout Successfully","response":response},status=200)

        except:
            return JsonResponse({"msg":"User or FCM token does not exists"})

@method_decorator(csrf_exempt,name='dispatch')
class SessionCheck(View):
    def post(self,request,*args, **kwargs):
        stream = io.BytesIO(request.body)
        python_data = JSONParser().parse(stream)

        try:
            user = CustomUser.objects.get(id=python_data['id'])
            data = FCMDevice.objects.get(user=user,fcm_token=python_data['fcm_token'])

            if data.active == True:
                return JsonResponse({"msg":data.active})
            else:
                return JsonResponse({"msg":data.active})

        except FCMDevice.DoesNotExist:
            return JsonResponse({'msg': 'FCM token not found'}, status=status.HTTP_404_NOT_FOUND)

@method_decorator(csrf_exempt,name='dispatch')
class GetSessionView(View):
    def post(self,request,*args, **kwargs):
        stream = io.BytesIO(request.body)
        python_data = JSONParser().parse(stream)

        try:
            user = CustomUser.objects.get(id=python_data['id'])
            userdata = FCMDevice.objects.filter(user=user)
            if userdata:
                serializer = FCMDeviceSerializer(userdata,many=True)
                return JsonResponse(serializer.data,safe=False)
            else:
                return JsonResponse({"msg":"No active device"})
        except:
            return JsonResponse({"msg":"User not Found"})

@method_decorator(csrf_exempt,name='dispatch')
class OrderAPI(View):

    def post(self,request,*args, **kwargs):
        stream = io.BytesIO(request.body)
        python_data = JSONParser().parse(stream)
        orderid = python_data['id']
        orderstatus = python_data['order_status']
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "order_status_updates",
            {
                "type":"send_order_status",
                "order_id":orderid,
                "order_status":orderstatus,
            }
        )
        return JsonResponse({"msg":"Order Updated Successfully"})


@method_decorator(csrf_exempt,name='dispatch')
class ResturantOff(View):
    def post(self,request,*args, **kwargs):
        stream = io.BytesIO(request.body)
        python_data = JSONParser().parse(stream)

        try:
            data_resturant = RestaurantName.objects.get(id=python_data['id'])
            data_resturant.status = False
            data_resturant.resturantoff = python_data['resturantoff']
            data_resturant.save()
            return JsonResponse({"msg":"Complete change"})

        except:
            return JsonResponse({"msg":"Data not found"})

@method_decorator(csrf_exempt,name='dispatch')
class ResturantWorking(View):
    def post(self,request,*args, **kwargs):
        stream = io.BytesIO(request.body)
        python_data = JSONParser().parse(stream)

        current_date = datetime.date.today()
        database_date_store = RestaurantName.objects.get(id=python_data['id'])
        database_date = database_date_store.resturantoff
        print(current_date)
        print(database_date)

        return JsonResponse({"msg":"Date shown"})


