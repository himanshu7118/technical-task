from django.db import models
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from django.core.validators import MinValueValidator, MaxValueValidator
import random, string
import datetime


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, fname, lname, password=None):
        if not email:
            raise ValueError('user must have an email address!')
        if not username:
            raise ValueError('user must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            fname=fname,
            lname=lname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, fname, lname, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            fname=fname,
            lname=lname,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserRegister(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=150, unique=True)
    username = models.CharField(max_length=50, unique=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fname', 'lname']

    objects = MyUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def randomNo():
    return random.randint(0,9999)

class Product_category(models.Model):
    category_id = models.IntegerField(null=False, blank=True, default=randomNo)
    category_name = models.CharField(null=False, blank=True, max_length=200)
    category_description = models.CharField(null=True, blank=True, max_length=200)
    product_thumbnail = models.FileField(blank=True, null=True, upload_to='Images/ProductCategoriesImage')
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.category_name

    @property
    def products(self):
        return self.product_set.all()

    @property
    def product_thumbnail_URL(self):
        try:
            url = self.product_thumbnail.url
        except:
            url = ''
        return url


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            self.created_at = datetime.datetime.now()
            product_category_save = super(Product_category, self).save(force_insert=False, force_update=False,
                                                                       using=None,
                                                                       update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            product_category_save = super(Product_category, self).save(force_insert=False, force_update=False,
                                                                       using=None,
                                                                       update_fields=None)
        return product_category_save


class Product(models.Model):
    product_id = models.CharField(default=randomNo, null=False, blank=True, max_length=100, unique=True)
    product_category_id = models.ForeignKey(Product_category, on_delete=models.SET_NULL, null=True, blank=True) # models.CASCADE
    product_name = models.CharField(null=False, blank=True, max_length=200)
    product_description = models.CharField(null=False, blank=False, max_length=200)
    product_images = models.FileField(db_column='product_images', blank=True, null=True, upload_to='Images/ProductImages')
    product_price = models.FloatField(null=True)
    gst = models.IntegerField(null=True, blank=True, default=0)
    product_status = models.CharField(null=False, blank=False, max_length=200)
    discount = models.FloatField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    # product_Subscribe = models.ForeignKey(Product_Subscribe, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def product_images_URL(self):
        try:
            url = self.product_images.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.product_name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            self.product_id = randomNo
            self.created_at = datetime.datetime.now()
            product_save = super(Product, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            product_save = super(Product, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        return product_save

class Offer(models.Model):
    offer_start_date = models.DateTimeField(null=True, blank=True)
    offer_end_date = models.DateTimeField(null=True, blank=True)
    offer_title_name = models.CharField(null=True, blank=True, max_length=200)
    offers_on_product = models.IntegerField(null=True, blank=True)
    offer_post = models.CharField(null=True, blank=True, max_length=800)
    offer_description = models.CharField(null=True, blank=True, max_length=1000)
    promo_code = models.CharField(null=True, blank=True, max_length=100, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0, null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:

            self.created_at = datetime.datetime.now()
            offer = super(Offer, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        else:
            self.updated_at = datetime.datetime.now()
            offer = super(Offer, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        return offer


class Order(models.Model):
    order_id = models.CharField(default=randomNo, null=False, blank=True, max_length=100, unique=True)
    user_id = models.ForeignKey(UserRegister, on_delete=models.SET_NULL, null=True, blank=True)
    order_value = models.FloatField(null=True, blank=True)
    offer_Id = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.FloatField(null=True, blank=True, default=0.0)
    payable_amount = models.FloatField(null=True, blank=True)
    payment_mode_choices = (
        ('wallet', 'wallet'),
        ('cod', 'cod'),
        ('debit_card', 'debit_card'),
        ('credit_card', 'credit_card'),
    )
    payment_mode = models.CharField(null=True, blank=True, max_length=20, choices=payment_mode_choices)
    order_status_choices = (
        ('book', 'book'),
        ('pending', 'pending'),
        ('In Stock', 'In Stock'),
        ('Out Of Range', 'Out Of Range'),
        ('Cancelled By Customer', 'Cancelled By Customer'),
    )
    order_status = models.CharField(null=True, blank=True, max_length=100, choices=order_status_choices, default='book')
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    subTotal = models.FloatField(null=True, blank=True, default=0.0)
    deliveryCharges = models.FloatField(null=True, blank=True, default=25.0)
    taxCharges = models.FloatField(null=True, blank=True, default=0.0)
    discountCouponCode = models.CharField(null=True, blank=True, max_length=100)
    grandTotal = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return self.order_id

    @property
    def get_cart_total_discount(self):
        orderitems = self.order_product_list_set.all()
        total = round(sum([item.get_total for item in orderitems]), 2)
        if self.offer_Id is not None:
            discount = round((total * (self.offer_Id.discount / 100)), 2)
            return discount
        else:
            return 0.0

    @property
    def get_cart_total_GST(self):
        orderitems = self.order_product_list_set.all()
        totalGst = round(sum([item.get_totalGST for item in orderitems]), 2)

        print("cart total gst")
        print(totalGst)
        return totalGst

    @property  # get_cart_sub_total
    def get_cart_total(self):
        print("ok in gst")
        orderitems = self.order_product_list_set.all()
        total = round(sum([item.get_total for item in orderitems]), 2)
        # totalGst = round((total * (18 / 100)), 2)
        totalGst = round(sum([item.get_totalGST for item in orderitems]), 2)
        # print(total)

        if self.offer_Id is not None:
            print("in in offer id")
            discount = round((total * (self.offer_Id.discount / 100)), 2)
            subTotal = total + totalGst + self.deliveryCharges - discount
            print(subTotal)
            print("delivery charges")
            print(self.deliveryCharges)
            return subTotal
        else:
            subTotal = total + totalGst + self.deliveryCharges
            print("delivery charges")
            print(self.deliveryCharges)
            print(subTotal)
            return subTotal

    @property  # get_cart_total
    def get_cart_sub_total(self):
        orderitems = self.order_product_list_set.all()
        total = round(sum([item.get_total for item in orderitems]), 2)
        return total

    @property
    def get_cart_quantities(self):
        orderitems = self.order_product_list_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.order_product_list_set.all().count()
        # total = sum([item.quantity for item in orderitems])
        total = orderitems
        return total

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None:
            # self.created_at = datetime.datetime.now()
            self.created_at = datetime.now()
            self.order_id = randomNo
            order_save = super(Order, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        else:
            # self.updated_at = datetime.datetime.now()
            self.updated_at = datetime.now()
            # self.order_id = randomword(5)
            order_save = super(Order, self).save(force_insert=False, force_update=False, using=None,
                                                     update_fields=None)
        return order_save

class Order_Product_List(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    product_price = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


