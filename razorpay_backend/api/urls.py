from django.urls import path
from .api_razorpay import RazorpayOrderAPIView, TransactionAPIView, FailedAPIView
from .api_payoneer import PayoneerOrderAPIView
urlpatterns = [
    path("razorpay/order/create/", 
        RazorpayOrderAPIView.as_view(), 
        name="razorpay-create-order-api"
    ),
    path("razorpay/order/complete/", 
        TransactionAPIView.as_view(), 
        name="razorpay-complete-order-api"
    ),
    path("razorpay/order/failed/", 
        FailedAPIView.as_view(), 
        name="razorpay-failed-order-api"
    ),
    path("payoneer/order/create/", 
        PayoneerOrderAPIView.as_view(), 
        name="payoneer-create-order-api"
    ),
]
