from rest_framework import serializers
from ..models import Transaction

# Serializer for creating a Razorpay order

class RazorpayOrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    currency = serializers.CharField()

class PayoneerOrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    currency = serializers.CharField()
    transactionId = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    street = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    zip = serializers.CharField(max_length=10)
    firstname = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=255)

class TranscationModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ['product', 'payment_id', 'order_id', 'signature', 'created_at', 'success_at', 'failed_at', 'status']
        read_only_fields = ['created_at'] 

    def get_amount(self, obj):
        return float(obj.amount)

class FailedOrderSerializer(serializers.Serializer):
    product = serializers.IntegerField()

