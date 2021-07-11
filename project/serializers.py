from django.db import models
from django.db.models import fields
from rest_framework import serializers

from project.models import UserRegister,Product,Product_category,Offer,Order,Order_Product_List


class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserRegister
        fields = ('id', 'email', 'username', 'fname', 'lname', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        data = UserRegister(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            fname=self.validated_data['fname'],
            lname=self.validated_data['lname'],
        )
        password=self.validated_data['password']
        data.set_password(password)
        data.save()
        return data
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True, required=True
    )

    class Meta:
        model = UserRegister
        fields = (
            'email',
            'password'
        )

class ProductSerializer(serializers.ModelSerializer):

    product_category_id = serializers.RelatedField(source='Product_category',read_only=True)

    class Meta:
        models = Product
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        models = Product_category
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        models = Offer
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):

    user_id = serializers.RelatedField(source='UserRegister',read_only=True) 
    offer_Id = serializers.RelatedField(source='Offer',read_only=True) 

    class Meta:
        models = Order
        fields = '__all__'

class Order_Product_ListSerializer(serializers.ModelSerializer):

    order_id = serializers.RelatedField(source='Order',read_only=True) 
    product_id = serializers.RelatedField(source='Product',read_only=True) 

    class Meta:
        models = Order_Product_List
        fields = '__all__'




