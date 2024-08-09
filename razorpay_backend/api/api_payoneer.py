from rest_framework.views import APIView
from rest_framework import status
from .razorpay_serializers import PayoneerOrderSerializer, TranscationModelSerializer
from rest_framework.response import Response
from razorpay_backend.api.payoneer.main import PayoneerClient
from ..models import Product, Transaction
from django.utils import timezone  

pa_client = PayoneerClient()

def VerifyTransaction(product, amount, payment_id, verify_order):
    if verify_order.get("status.code") == "success":
        transactionSerializer = TranscationModelSerializer(data={
            "product": product,
            "amount": amount,
            "payment_id": payment_id,
            "order_id": verify_order.get("order_id"),
        })

        if transactionSerializer.is_valid():
          Transaction.objects.create(
            product=product,
            amount=amount,
            payment_id=payment_id,
            order_id=verify_order.get("order_id"),
            signature=None,
            created_at=timezone.now(),
            status='success',
            failed_at=None,
            success_at=timezone.now()
        )   
        
    else:
        Transaction.objects.create(
            product=product,
            amount=amount,
            payment_id=payment_id,
            order_id=None,
            signature=None,
            created_at=timezone.now(),
            status='failed',
            failed_at=timezone.now(),
            success_at=None
        )

class PayoneerOrderAPIView(APIView):
  """This API will create an order"""

  def post(self,request):
    order_serializer = PayoneerOrderSerializer(data=request.data)

    if order_serializer.is_valid():
      product_id = order_serializer.validated_data.get("product_id")

      try:
        product = Product.objects.get(id=product_id)
        amount = float(product.amount)
        print("Got the product from database")

        try:
          order_response = pa_client.create_order(
            amount=amount,
            currency=order_serializer.validated_data.get("currency"),
            transactionId=order_serializer.validated_data.get("transactionId"),
            country=order_serializer.validated_data.get("country"),
            email=order_serializer.validated_data.get("email"),
            street=order_serializer.validated_data.get("street"),
            city=order_serializer.validated_data.get("city"),
            zip=order_serializer.validated_data.get("zip"),
            firstname=order_serializer.validated_data.get("firstname"),
            lastname=order_serializer.validated_data.get("lastname"),
          )
          
          print("Order Created")

          payment_id = order_response.get("payment.invoiceId")
          listId = order_response.get("links.self")

          verify_order = pa_client.verify_payment(listId)

          print("Order Verified",verify_order)

          VerifyTransaction(product, amount, payment_id, verify_order)

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
        "error": order_serializer.errors
      }
      return Response(response, status=status.HTTP_400_BAD_REQUEST)