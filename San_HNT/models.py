
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import  (
    AbstractUser, Permission, Group
)

class Role(models.TextChoices):
    CUSTOMER = "Cá nhân", "Customer"
    ADMIN = "admin", "Admin"
    EMPLOYEE = "Nhân viên", "Employee"
    SUPPLIER = "Tiểu thương hoặc danh nghiệp", "Supplier"

class TypePay(models.TextChoices):
    TIENMAT = "tienmat", "TienMat"
    ONLINE = "online", "Online"


class StateOrder(models.TextChoices):
    WAITXACNHAN = "choxacnhan" , "ChoXacNhan"
    XACNHAN = "xacnhan" , "XacNhan"
    CHOGIAOHANG = "chogiaohang" , "ChoGiaoHang"
    HUY = "huy" , "Huy"
    DAHUY = "dahuy" , "DaHuy"
    DAGIAO = "dagiao" , "DaGiao"

# class CloudinaryField(BaseCloudinaryField):
#     def upload_options(self, model_instance):
#         return {
#             'public_id': model_instance.name,
#             'unique_filename': False,
#             'overwrite': True,
#             'resource_type': 'image',
#             'tags': ['map', 'market-map'],
#             'invalidate': True,
#             'quality': 'auto:eco',
#         }



class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True, blank=True)
    address= models.CharField(max_length= 200 ,default = '')
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CUSTOMER)
    groups = models.ManyToManyField(Group)



    def __str__(self):
        return self.username
class Phone(models.Model):
    phoneID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    number = models.CharField( max_length=11)

    def __str__(self):
        return self.phoneID



class BaseModel(models.Model):
    NgayTao = models.DateTimeField(auto_now_add=True)
    NgayUpdate = models.DateTimeField(auto_now=True)
    Active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Customer(models.Model):
    Customer = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.Customer.__str__()

class Comment(BaseModel):
    CommentID = models.AutoField(primary_key=True)
    Content = models.CharField(max_length=200)
    Customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    Reply = models.ForeignKey('self', on_delete=models.CASCADE, null = True, blank=True)
    IDEdComment = models.CharField(max_length=20)


    def __str__(self):
        return self.CommentID.__str__()

class CommentImage(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    image = CloudinaryField(
        "Image",
        null= True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)



class Supplier(BaseModel):
    Supplier = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Active_Store = models.BooleanField( default= False, null = True)
    CompanyName = models.CharField( max_length= 100, null = True)
    TotalComment = models.IntegerField(default=0)
    TotalRating = models.FloatField(default=0.0)
    categorys = models.ManyToManyField('Category')
    Description = models.TextField(null= True, blank=True)


    def __str__(self):
        return self.Supplier.__str__()





class Category(BaseModel):
    CategoryID = models.AutoField( primary_key=True)
    CategoryName = models.CharField(max_length=100)
    Description = models.TextField(null= True, blank=True)

    def __str__(self):
        return self.CategoryName








class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    image = CloudinaryField(
        "Image",
        null= True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Product(BaseModel):
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=100)

    Category = models.ForeignKey('Category', on_delete=models.CASCADE)
    Supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE )
    UnitPrice = models.FloatField( default=0.0)
    Description = models.TextField(null = True, blank=True)

    NumberInStore = models.IntegerField(default=1)
    NumberBuyed= models.IntegerField(default=0)


    def __str__(self):
        return f"{self.ProductID} - {self.UnitPrice}"





class Order(BaseModel):
    OrderID = models.AutoField( primary_key=True)
    Customer = models.ForeignKey('Customer', on_delete=models.PROTECT)
    TypePay = models.CharField(max_length=10, choices=TypePay.choices, default=TypePay.ONLINE)
    StateOrder = models.CharField( max_length=20 , choices=StateOrder.choices, default=StateOrder.WAITXACNHAN)

    def __str__(self):
        return str(self.OrderID)


class OrderDetail(models.Model):
    OrderDetailID = models.AutoField(primary_key=True)
    Quantity = models.IntegerField()
    UnitPrice = models.FloatField(default=0.0)
    Discount = models.FloatField()
    Order = models.ForeignKey('Order', on_delete=models.PROTECT)
    Product = models.ForeignKey('Product', on_delete=models.PROTECT)


    def __str__(self):
        return str(self.OrderDetailID)


class Deals(BaseModel):
    DealID = models.AutoField(primary_key=True)
    Supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    DealName = models.CharField( max_length=200 )
    Discount = models.FloatField()
    EndDate = models.DateTimeField()
    Description = models.TextField(null = True, blank=True)
    CategoryID = models.OneToOneField( 'Category' , on_delete=models.CASCADE,  null = True)