from xml.dom import ValidationErr
from rest_framework.views import APIView
from rest_framework import status
from .razorpay_serializers import RazorpayOrderSerializer, TranscationModelSerializer, FailedOrderSerializer
from razorpay_backend.api.razorpay.main import RazorpayClient
from rest_framework.response import Response
from ..models import Product, Transaction
from django.utils import timezone  

rz_client = RazorpayClient()

class RazorpayOrderAPIView(APIView):
    """This API will create an order"""
    
    def post(self, request):
        razorpay_order_serializer = RazorpayOrderSerializer(data=request.data)

        if razorpay_order_serializer.is_valid():
            product_id = razorpay_order_serializer.validated_data.get("product_id")
            
            try:
                product = Product.objects.get(id=product_id)
                amount = float(product.amount) 

                try:
                    order_response = rz_client.create_order(
                        amount=amount,
                        currency=razorpay_order_serializer.validated_data.get("currency")
                    )
                    response = {
                        "status_code": status.HTTP_201_CREATED,
                        "message": "order created",
                        "data": order_response
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
                except Exception as e:
                    Transaction.objects.create(
                        product=product,
                        amount=amount,
                        payment_id=None,
                        order_id=None,
                        signature=None,
                        status='failed',
                        failed_at=timezone.now()  
                    )
                    response = {
                        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "message": "order creation failed",
                        "error": str(e)
                    }
                    return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Product.DoesNotExist:
                return Response({
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Product not found"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": razorpay_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TransactionAPIView(APIView):
    """This API will complete order and save the 
    transaction"""
    
    def post(self, request):
        transaction_serializer = TranscationModelSerializer(data=request.data)
        if transaction_serializer.is_valid():
            data = transaction_serializer.validated_data
            product_id = data.get("product")

            product_id = product_id.id
            product = Product.objects.get(id=product_id)
            amount = float(product.amount)  

            transaction = Transaction.objects.create(
                product=product,
                amount=amount,
                payment_id=data.get("payment_id"),
                order_id=data.get("order_id"),
                signature=data.get("signature"),
                status='pending',  
                success_at=None, 
                failed_at=None    
            )

            try:
                rz_client.verify_payment_signature(
                    razorpay_payment_id=data.get("payment_id"),
                    razorpay_order_id=data.get("order_id"),
                    razorpay_signature=data.get("signature")
                )
                
                transaction.status = 'success'
                transaction.success_at = timezone.now()
                transaction.save()

                response = {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "transaction created",
                    "data": TranscationModelSerializer(transaction).data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            except ValidationErr as e:
                transaction.status = 'failed'
                transaction.failed_at = timezone.now()
                transaction.save()

                response = {
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "transaction verification failed",
                    "error": str(e)
                }
                return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": transaction_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
class FailedAPIView(APIView):
    """This API will complete order and save the 
    transaction"""
    
    def post(self, request):
        transaction_serializer = FailedOrderSerializer(data=request.data)
        if transaction_serializer.is_valid():
            data = transaction_serializer.validated_data
            product_id = data.get("product")
            product = Product.objects.get(id=product_id)
            amount = float(product.amount) 

            Transaction.objects.create(
                product=product,
                amount=amount,
                payment_id=None,
                order_id=None,
                signature=None,
                created_at=timezone.now(),
                status='failed',  
                success_at=None, 
                failed_at = timezone.now(),
            )

            response = {
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "transation failed successfully",
                "error": transaction_serializer.errors
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "transation failed",
                "error": transaction_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)