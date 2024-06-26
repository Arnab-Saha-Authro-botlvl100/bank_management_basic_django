from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    ACCOUNT_TYPES = (
        ('savings', 'Savings'),
        ('checking', 'Checking'),
       
    )

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    account_number = models.CharField(max_length=20, unique=True, null=True, blank=True)  # Allow null initially
    account_holder_name = models.CharField(max_length=20, null=True, blank=True)  # Allow null initially
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Allow null initially
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)  # Allow null initially
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user.username} - {self.account_number}'

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f"{self.account.user.username} - {self.amount} - {self.transaction_type}"
