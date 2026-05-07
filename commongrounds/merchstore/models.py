from django.conf import settings
from django.db import models


class Profile(models.Model):
    """User profile for role-based access and event ownership."""
    ROLE_MEMBER = 'Member'
    ROLE_SELLER = 'Market Seller'
    ROLE_CHOICES = [
        (ROLE_MEMBER, 'Member'),
        (ROLE_SELLER, 'Market Seller'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=ROLE_MEMBER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "product types"


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    product_image = models.ImageField(
        upload_to = 'merchstore/products/',
        null=True,
        blank=True
    )
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=10)
    stock = models.PositiveIntegerField()
    PRODUCT_STATUS_AVAILABLE = 'Available'
    PRODUCT_STATUS_ON_SALE = 'On Sale'
    PRODUCT_STATUS_OUT_OF_STOCK = 'Out of Stock'
    PRODUCT_STATUS_CHOICES = [
        (PRODUCT_STATUS_AVAILABLE, 'Available'),
        (PRODUCT_STATUS_ON_SALE, 'On Sale'),
        (PRODUCT_STATUS_OUT_OF_STOCK, 'Out of Stock')
    ]
    status = models.CharField(
        max_length=20,
        choices=PRODUCT_STATUS_CHOICES,
        default=PRODUCT_STATUS_AVAILABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "products"


class Transaction(models.Model):
    buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    TRANSACITON_STATUS_ON_CART = 'On Cart'
    TRANSACITON_STATUS_TO_PAY = 'To Pay'
    TRANSACITON_STATUS_TO_SHIP = 'To Ship'
    TRANSACITON_STATUS_TO_RECEIVE = 'To Receive'
    TRANSACITON_STATUS_DELIVERED = 'Delivered'
    TRANSACTION_STATUS_CHOICES = [
        (TRANSACITON_STATUS_ON_CART, 'On Cart'),
        (TRANSACITON_STATUS_TO_PAY, 'To Pay'),
        (TRANSACITON_STATUS_TO_SHIP, 'To Ship'),
        (TRANSACITON_STATUS_TO_RECEIVE, 'To Receive'),
        (TRANSACITON_STATUS_DELIVERED, 'Delivered')
    ]
    status = models.CharField(
        max_length=20,
        choices=TRANSACTION_STATUS_CHOICES
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "transactions"
