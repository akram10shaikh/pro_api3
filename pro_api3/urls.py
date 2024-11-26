from django.contrib import admin
from django.urls import path, include
from myapp import views
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    # Restaurant Creation and updation
    path('restaurant/', MyRestaurantNameAPIView.as_view()),
    path('restaurant/<int:pk>/', MyRestaurantNameAPIView1.as_view()),

    # Order Creation and updation
    path('order/',MyOrderAPIView.as_view()),
    path('order/<int:pk>/',MyOrderAPIView1.as_view()),

    # Ticket Creation and updation
    path('ticket/',MyTicket_raiseAPIView.as_view()),
    path('ticket/<int:pk>/',MyTicket_raiseAPIView1.as_view()),

    # User creation and updation
    path('user/',MyCustomeUserAPIView.as_view()),
    path('user/<int:pk>/',MyCustomeUserAPIView1.as_view()),

    # Otp generation
    path('otp/',Otp.as_view()),

    # User checking using id
    path('user_check/',User_check.as_view()),

    # Authentication of the users
    path('auth/',include('rest_framework.urls')),

    # For index page
    path('index/',index),

    # Token checking the user
    path('token_check/',Token_check.as_view()),

    # Checking order status
    path('orderstatus/',OrderStatus.as_view()),
    path('orderStatusAPI/',OrderAPI.as_view()),

    # For order notification and websocket
    path('order_notification/',Order_Notification.as_view()),

    # Checking the firebase conncetion
    path('check_firebase_connection/', check_firebase_connection, name='check_firebase_connection'),

    # Order history
    path('order_history/',Order_History.as_view()),

    # Feedback page
    path('feedback/',MyFeedbackAPIView.as_view()),

    # Subscription of the user
    path('subscription/',MySubscriptionAPIView.as_view()),

    # restuarant checking
    path('restuarant_check/',RestaurantCheck.as_view()),

    # FCM token and device registration
    path('device_registration/',DeviceRegistrationAPIView.as_view()),
    path('device_registration/<int:pk>/',DeviceRegistrationAPIView1.as_view()),
    path('startsession/',StartSession.as_view()),
    path('sessioncheck/',SessionCheck.as_view()),
    path('logoutsession/',LogoutSession.as_view()),
    path('getsession/',GetSessionView.as_view()),

    # Terms and condition
    path('terms/', views.terms_and_conditions, name='terms_and_conditions'),
    path('policy/', views.privacy_policy, name='privacy_policy'),
    path('faq/', views.faq, name='faq'),
    path('restaurant/order-history/', RestaurantOrderHistory.as_view(), name='restaurant_order_history'),

    path('resturantoff/',ResturantOff.as_view()),
    path('resturantworking/',ResturantWorking.as_view()),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
