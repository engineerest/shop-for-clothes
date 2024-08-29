import uuid

from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group

from Landing.sozia.settings import AUTH_USER_MODEL as AUM
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)

    related_user = models.ForeignKey(AUM, on_delete=models.CASCADE, null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_user_permissions',
        blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Account(AbstractBaseUser, PermissionsMixin):
    user = models.OneToOneField(AUM, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, unique=True, null=False)
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=False, unique=False)
    city = models.CharField(max_length=255, unique=False, null=False)
    country = models.CharField(max_length=255, unique=False, null=False)
    groups = models.ManyToManyField(
        Group,
        related_name='account_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='account_user_permissions',
        blank=True
    )

    def __str__(self):
        return self.user

class Seller(AbstractBaseUser, PermissionsMixin):
    user = models.ForeignKey(AUM, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, null=False, unique=True)
    phone = models.CharField(max_length=255, null=False, unique=True)
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    is_superuser = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class ShopCategory(models.Model):
    user = models.ForeignKey(AUM, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')


    def __str__(self):
        return self.name

class ShopProduct(models.Model):
    user = models.ForeignKey(AUM, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(ShopCategory, on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(upload_to='images/')
    discount = models.DecimalField(max_digits=2, decimal_places=0)
    price_with_discount = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_cart = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(AUM, on_delete=models.CASCADE)
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class Checkout(models.Model):
    user = models.ForeignKey(AUM, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=255)
    order_name = models.CharField(max_length=255)
    product = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_name