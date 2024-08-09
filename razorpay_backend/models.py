from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE,default=1) 
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    payment_id = models.CharField(null=True,blank=True, max_length=255) 
    order_id = models.CharField(null=True,blank=True, max_length=255)  
    signature = models.CharField(null=True,blank=True, max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)  
    success_at = models.DateTimeField(null=True, blank=True)  
    failed_at = models.DateTimeField(null=True, blank=True)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Status of the transaction

    def __str__(self):
        return f"Transaction {self.id} - {self.product.name}"
