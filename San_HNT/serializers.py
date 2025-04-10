import uuid

import cloudinary.uploader

from rest_framework import serializers
from San_HNT.models import (Product , User, Role,  Permission, Category ,Product,
                            Supplier, Comment, OrderDetail, Customer, Order, CommentImage,
                            StateOrder, ProductImage, Deals)
from django.contrib.auth.models import Group




class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class StateOrderSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()

    @classmethod
    def get_state_orders(cls):
            return [{"CategoryName": choice.value, "CategoryID": choice.label} for choice in StateOrder]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['CommentID', 'Content', 'Customer' , 'Reply' , 'IDEdComment']


class MoneyField(serializers.FloatField):
    def to_representation(self, value):
        value = value * 1_000_000  # Nhân với 1 triệu
        return f"{value:,.0f} VND"



class ProductSerializer(serializers.ModelSerializer):
    UnitPrice = MoneyField()
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return [img.image.url for img in obj.productimage_set.all()]

    class Meta:
        model = Product
        fields = ['ProductID' , 'ProductName', 'UnitPrice', 'Description', 'NumberInStore', 'NumberBuyed', 'Category_id', 'Supplier_id' ,'images' ]



class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, source='Product')
    class Meta:
        model = OrderDetail
        fields = ['OrderDetailID', 'Quantity','UnitPrice','Discount','Order', 'product']


class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True, source='orderdetail_set')

    created_date = serializers.SerializerMethodField()

    def get_created_date(self, obj):
        return obj.NgayTao.strftime("%d/%m/%Y")

    class Meta:
        model = Order
        fields = [
            'OrderID', 'Customer', 'TypePay', 'StateOrder',
            'order_details', 'NgayTao', 'created_date',
        ]



class UserSerializer(serializers.ModelSerializer):


    def create(self, validated_data):

        role = validated_data.pop('role', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)

        if role == Role.SUPPLIER.value:
            role = Role.SUPPLIER.label
            print(role)

        else:
            role = Role.CUSTOMER.label
            print(role)

        avatar = validated_data.pop('avatar', None)
        print(type(avatar))
        #
        if avatar:
            uploaded_avatar = cloudinary.uploader.upload(avatar)
            avatar = uploaded_avatar.get("secure_url")
            print(avatar)

        user = User(role=role, avatar = avatar,first_name= first_name, last_name = last_name, **validated_data)
        user.set_password(user.password)

        user.save()

        group= Group.objects.get(name = "Người mua")
        user.groups.add(group)

        if role == Role.SUPPLIER.label:
            Supplier.objects.create(CompanyName = last_name + " " + first_name , Supplier=user)
        else:
            Customer.objects.create(Customer = user)


        return user

    avatar = serializers.SerializerMethodField()
    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None

    class Meta:
        model = User
        fields= [ 'id' , 'first_name', 'last_name' , 'address', 'avatar' , 'email' , 'username', 'password' , 'role' ]
        extra_Kwargs = {
            'password': { "write_only" : True}
        }

class PermissionSerializer( serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = ['CategoryID','CategoryName', 'Description' ]



class SupplierSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(source='Supplier_id')
    user = UserSerializer(source='Supplier')
    class Meta:
        model = Supplier
        fields = ['Supplier_id' , 'Active_Store','CompanyName', 'TotalComment','Description',  'TotalRating' , 'user' ]



class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model =  Customer
        fields = ['Customer_id' ]


class CommentImageSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    class Meta:
        model = CommentImage
        fields = [ 'id','avatar']

    def get_id(self, obj):
        return str(uuid.uuid4())

    def get_avatar(self, obj):
        if obj.image:
            return obj.image.url
        return None


class BasicCustomerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='Customer_id')
    user = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ['id', 'user']

    def get_user(self, obj):
        return {
            "id": obj.Customer.id,
            "username": obj.Customer.username,
            "avatar": obj.Customer.avatar.url
        } if obj.Customer else None


class BaseSupplierSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='Supplier_id')

    avatar = serializers.SerializerMethodField()
    class Meta:
        model = Supplier
        fields = ['id', 'avatar', 'TotalRating' , 'CompanyName', 'Description','TotalComment']


    def get_avatar(self, obj):
        return obj.Supplier.avatar.url if obj.Supplier and obj.Supplier.avatar else None
    # def get_user(self, obj):
    #     return {
    #          "id": obj.Supplier.id,
    #          "avatar": obj.Supplier.avatar.url
    #     } if obj.Supplier else None



class DealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deals
        fields = '__all__'