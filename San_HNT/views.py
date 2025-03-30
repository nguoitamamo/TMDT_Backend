from pickle import FALSE

from django.contrib.auth import authenticate
from django.core.serializers import serialize
from django.http import HttpResponse
from django.http.multipartparser import MultiPartParser
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics, parsers, status
from San_HNT.models import (Product, User, Permission, Category,
                            Supplier, ProductImage, Comment, OrderDetail,
                            StateOrder, Customer, Order, CommentImage)
from rest_framework.decorators import action, permission_classes
from django.contrib.auth.models import Group
from .serializers import (
    ProductSerializer, UserSerializer, PermissionSerializer, CategorySerializer,
    SupplierSerializer, CommentSerializer, OrderDetailSerializer, TopSupplierSerializer,
    CustomerSerializer, OrderSerializer, BasicCustomerSerializer, CommentImageSerializer)
import cloudinary.uploader
from .perms import OwnerPerms, IsUserSelf
from .paginators import ProductPaginator, CommentPaginator
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from oauth2_provider.models import AccessToken


def index(request):
    return HttpResponse(
        "heelo huynh ngoc truong"
    )



class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer


class CommentViewSet(viewsets.ModelViewSet, generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.filter(Active=True).all()
    serializer_class = CommentSerializer
    pagination_class = CommentPaginator


    @action(methods=['get'], detail= False, url_path='baseinfo')
    def base_info(self, request):
        id = request.query_params.get('id', None)
        key = request.query_params.get('key', None)

        if not id:
            return Response({"error": "Thiếu tham số id"}, status=status.HTTP_400_BAD_REQUEST)

        if key:
            comment = Comment.objects.filter(IDEdComment=id).first()
            commentImage = CommentImage.objects.filter(comment=comment)
            results ={}

            customer = comment.Customer
            results['comment'] = CommentSerializer(comment).data
            results['comment']['Customer'] = BasicCustomerSerializer(customer).data
            results['image'] = CommentImageSerializer(commentImage,  many=True).data

            return Response(results, status = status.HTTP_200_OK)


    @action(methods=['get'], detail=False)
    def get_comment_ed(self, request):
        id = request.query_params.get('id', None)
        key = request.query_params.get('key', None)

        if not id:
            return Response({"error": "Thiếu tham số id"}, status=status.HTTP_400_BAD_REQUEST)

        if key:
            comments = Comment.objects.filter(IDEdComment=id).first()
            return Response(CommentSerializer(comments).data, status = status.HTTP_200_OK)

        comments = Comment.objects.filter(IDEdComment=id).all()
        comments_tmp = list(comments)  # Chuyển về list để dễ thao tác
        comment_lookup = {}
        grouped_comments = []

        while len(comments_tmp) > 0:
            for comment in comments_tmp[:]:
                customer = comment.Customer
                comment_images = CommentImage.objects.filter(comment=comment)

                comment_data = CommentSerializer(comment).data
                comment_data["Customer"] = BasicCustomerSerializer(customer).data
                comment_data["image"] = CommentImageSerializer(comment_images, many=True).data
                comment_data["replies"] = []

                comment_lookup[comment.CommentID] = comment_data

                if comment.Reply is None:
                    grouped_comments.append( comment_data)
                    comments_tmp.remove(comment)  # Xóa comment đã xử lý
                else:
                    parent_id = comment.Reply.CommentID
                    if parent_id in comment_lookup:
                        comment_lookup[parent_id]["replies"].append(comment_data)
                        comments_tmp.remove(comment)  # Xóa comment đã xử lý

        return Response(grouped_comments, status=status.HTTP_200_OK)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPaginator

    def get_queryset(self):
        query = self.queryset

        name = self.request.query_params.get('name')

        if name:
            query = query.filter(ProductName__icontains=name)

        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        print(min_price, type(min_price))
        print(max_price, type(max_price))
        print(float(min_price))
        print(float(max_price))

        print(float('1.9'))

        if min_price:
            query = query.filter(UnitPrice__gte=float(min_price))
        if max_price:
            query = query.filter(UnitPrice__lte=float(max_price))

        company_name = self.request.query_params.get('company_name')

        supplier_ids = Supplier.objects.filter(CompanyName__icontains=company_name, Active_Store=True).values_list(
            "Supplier", flat=True)

        if supplier_ids:
            query = query.filter(Supplier__in=supplier_ids)

        sort = self.request.query_params.get('sort')
        if sort == 'name':
            query = query.order_by('ProductName')
        elif sort == 'price':
            query = query.order_by('UnitPrice')

        return query

    @action(methods=['get'], detail=False, url_path='search')
    def search_products(self, request):
        products = self.get_queryset()
        print(products)

        paginator = ProductPaginator()
        page = paginator.paginate_queryset(products, request)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='top')
    def get_products_top(self, request):
        top_suppliers = list(Supplier.objects.filter(TotalRating__gt=4.0).order_by('-TotalRating')[:3])

        products = Product.objects.filter(Supplier__in=top_suppliers).order_by('-NumberBuyed')[:3]

        for x in products:
            print([img.image.url for img in x.productimage_set.all()])


        return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'POST'] and self.action in ['add_store', 'get_rate' ,'logout_user']:
            return [OwnerPerms()]

        return [permissions.AllowAny()]

    @action(methods=['post'], url_path='signup', detail=False)
    def Signup_user(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], url_path='login', detail=False)
    def login_user(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)


        if user is not None:

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Thông tin đăng nhập không hợp lệ!"}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail= False, url_path='logout')
    def logout_user(self,request):
        token = request.data.get("token")
        print(token)
        # Lấy token từ request
        if token:
            try:
                access_token = AccessToken.objects.get(token=token)
                access_token.delete()  # Xóa token khỏi database
                return Response({"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK)
            except AccessToken.DoesNotExist:
                return Response({"error": "Token không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Không tìm thấy token"}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get' , 'patch'], url_path='current-user', detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        user = request.user
        serializer = UserSerializer(user)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='permissions', detail=True)
    def get_permissions_user(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)

            all_permissions = user.get_all_permissions()

            codenames = [x.split('.')[1] for x in all_permissions]

            permission_queryset = Permission.objects.filter(codename__in=codenames)

            seen_codenames = set()
            permission_list = []

            for p in permission_queryset:
                if p.codename not in seen_codenames:
                    permission_list.append({"name": p.name, "codename": p.codename, "id": p.id})
                    seen_codenames.add(p.codename)

            return Response({"permissions": permission_list}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='uploadimage', permission_classes=[permissions.IsAuthenticated])
    def upload_image(self, request):
        image = request.data.get('image')
        if image:
            uploaded_avatar = cloudinary.uploader.upload(image)
            avatar = uploaded_avatar.get("secure_url")
            return Response({"imageCloud": avatar}, status.HTTP_200_OK)
        return Response({"error": "khong the tai anh!"}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], url_path='add_store/(?P<category_id>[^/.]+)', detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def add_store(self, request, pk=None, category_id=None):
        try:

            supplier = Supplier.objects.get(Supplier_id=pk)
            category = Category.objects.get(CategoryID=category_id)
        except Supplier.DoesNotExist:
            return Response({"error": "Supplier không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "Category không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        product_name = request.data.get('ProductName')
        number_input = int(request.data.get('NumberInStore', 0))
        serializer = ProductSerializer(data=request.data)

        existing_product = Product.objects.filter(ProductName=product_name, Supplier_id=pk,
                                                  Category_id=category_id).first()

        if existing_product:
            existing_product.NumberInStore += number_input
            existing_product.save()
            product = existing_product
        else:
            if serializer.is_valid():
                product = serializer.save(Category=category, Supplier=supplier)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image_filenames = request.data.getlist('list_image')

        for name_image in image_filenames:
            uploaded_avatar = cloudinary.uploader.upload(name_image)
            avatar = uploaded_avatar.get("secure_url")
            productImage = ProductImage(product_id=product.id, image=avatar)
            productImage.save()

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer





class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer






    @action(methods=['get'], detail=True, url_path='suggest')
    def suggest_product(self, request, pk=None):
        customer = self.get_object()


        bought_products = Product.objects.filter(
            orderdetail__Order__Customer__Customer=customer
        )

        category_ids = bought_products.values_list("Category_id", flat=True).distinct()
        supplier_ids = bought_products.values_list("Supplier_id", flat=True).distinct()

        related_products = Product.objects.filter(
            Q(Category_id__in=category_ids) | Q(Supplier_id__in=supplier_ids)
        )

        serializer = ProductSerializer(related_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    # @action(methods=['get'], detail=True, permission_classes=[permissions.IsAuthenticated])
    # def get_permissions(self, request, pk=None):
    #     try:
    #         # Lấy thông tin user theo ID
    #         user = User.objects.get(pk=pk)
    #
    #         # Lấy tất cả các quyền của user (cả quyền cá nhân và từ nhóm)
    #         user_permissions = user.get_all_permissions()
    #
    #         return Response({"user_id": user.id, "permissions": list(user_permissions)})
    #     except User.DoesNotExist:
    #         return Response({"error": "User not found"}, status=404)


class CategoryViewSet(viewsets.ModelViewSet, generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['post'], url_path='create', detail=True, permission_classes=[permissions.IsAuthenticated])
    def create_category(self, request, pk=None):
        try:
            supplier = Supplier.objects.get(Supplier_id=pk)
        except Supplier.DoesNotExist:
            return Response({"error": "Không tìm thấy nhà cung cấp"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            category = serializer.save()
            supplier.categorys.add(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH'] or self.action in ['xacnhan_dk_banhang', 'get_rate']:
            return [OwnerPerms()]

        return [permissions.AllowAny()]

    @action(methods=['patch'], detail=True, url_path='xacnhan_dk_banhang')
    def xacnhan_dk_banhang(self, request, pk=None):
        supplier = self.get_object()

        if not supplier:
            return Response({"status": False, "error": "Supplier not found"}, status=status.HTTP_400_BAD_REQUEST)

        supplier.Active_Store = True
        supplier.save()

        user = supplier.Supplier

        group = Group.objects.get(name='Người bán')

        user.groups.add(group)
        user.save()

        return Response({"status": supplier.Active_Store}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['patch'], detail=True, url_path='add_rate')
    def get_rate(self, request, pk=None):
        number_rate = float(request.query_params.get("number_rate"))

        if not number_rate:
            return Response({"error": "Number_rate !!!"}, status=400)

        supplier = self.get_object()
        if not supplier:
            return Response({"message": "Không có nhà cung cấp nào"}, status=404)

        supplier.TotalRating = (supplier.TotalRating * supplier.TotalComment + number_rate) / (
                supplier.TotalComment + 1)
        supplier.TotalComment += 1
        supplier.save()

        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='info_short' )
    def get_supplier(self,request, pk = None):
        print("đã và đây")
        return Response(TopSupplierSerializer(self.get_object()).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='top')
    def get_top_supplier(self, request):
        suppliers = Supplier.objects.filter(TotalRating__gt=4.0).order_by('-TotalRating')[:3]

        return Response(TopSupplierSerializer(suppliers, many=True).data, status=status.HTTP_200_OK)


    @action(methods=['get'], detail=True, url_path='thongke')
    def thong_ke(self, request, pk = None):

        filter_type = request.query_params.get('filter', None)
        month = request.query_params.get('month', None)
        year = request.query_params.get('year', None)
        quarter = request.query_params.get('quarter', None)

        if  pk and filter_type:
            try:
                supplier = self.get_object()
            except Supplier.DoesNotExist:
                return Response({"error": "khon tìm thấy Supplier!"}, status=status.HTTP_404_NOT_FOUND)

            now = timezone.now()

            if filter_type == "month":
                month = now.month if month is None else month

                results = OrderDetail.objects.filter(
                    Product__Supplier=supplier,
                    Order__NgayTao__year=now.year,
                    Order__NgayTao__month=month
                ).annotate(time=TruncMonth('Order__NgayTao')).values(
                    'time', 'Product__ProductName'
                ).annotate(
                    total_products=Sum('Quantity'),
                    total_money = Sum(F('Quantity') * F('UnitPrice') * (1 - F('Discount'))) ,
                    total_order =Count('OrderDetailID')

                )

            elif filter_type == "quarter":
                dic = {
                    "1" : ["1" ,"3"],
                    "2" : [ "4", "6"],
                    "3" : ["7", "9"],
                    "4" : ["10", "12"]
                }
                quarter = quarter = dic.get(quarter, None)
                results = OrderDetail.objects.filter(
                    Product__Supplier=supplier,
                    Order__NgayTao__year=now.year,
                    Order__NgayTao__month__range = quarter

                ).annotate(time=TruncQuarter('Order__NgayTao')).values(
                    'time'
                ).annotate(
                    total_products=Sum('Quantity'),
                    total_money=Sum(F('Quantity') * F('UnitPrice') * (1 - F('Discount'))),
                    total_order=Count('OrderDetailID')
                )

            elif filter_type == "year":
                year = now.year if year is None else year
                results = OrderDetail.objects.filter(
                    Product__Supplier=supplier,
                    Order__NgayTao__year=year
                ).annotate(time=TruncYear('Order__NgayTao')).values(
                    'time', 'Product__ProductName'
                ).annotate(
                    total_products=Sum('Quantity'),
                    total_money=Sum(F('Quantity') * F('UnitPrice') * (1 - F('Discount'))),
                    total_order=Count('OrderDetailID')
                )


            return Response({
                "Supplier": supplier.CompanyName,
                "Results": results
            })


    @action(methods=['get'], detail=False, url_path='get_store_not_active')
    def get_store_not_active(self, request):
        supplier = Supplier.objects.filter(Active_Store=False)
        return Response({"ds_suppliers": SupplierSerializer(supplier, many=True).data, }, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get_category')
    def get_category_supplier(self, request, pk=None):
        supplier = Supplier.objects.filter(Supplier_id=pk).first()
        if not supplier:
            return Response({"error": "Không tìm thấy supplier!"}, status=status.HTTP_400_BAD_REQUEST)

        categories = supplier.categorys.all()

        category_data = [{"id": c.id, "name": c.name} for c in categories]

        return Response({"supplier": SupplierSerializer(supplier).data, "categories": category_data},
                        status=status.HTTP_200_OK)
