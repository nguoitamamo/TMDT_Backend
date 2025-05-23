
from django.contrib.auth import authenticate
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics, parsers, status
from San_HNT.models import (Product, User, Permission, Category,
                            Supplier, ProductImage, Comment, OrderDetail,
                            StateOrder, Customer, Order, CommentImage, StateOrder,Deals)
from rest_framework.decorators import action, permission_classes
from django.contrib.auth.models import Group
from rest_framework.utils.mediatypes import order_by_precedence

from .serializers import (
    ProductSerializer, UserSerializer, PermissionSerializer, CategorySerializer,
    SupplierSerializer, CommentSerializer, OrderDetailSerializer, BaseSupplierSerializer,
    CustomerSerializer, OrderSerializer, BasicCustomerSerializer, CommentImageSerializer,
    StateOrderSerializer, DealsSerializer)
import cloudinary.uploader
from .perms import OwnerPerms, EmployeePermission
from .paginators import ProductPaginator, CommentPaginator
from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from oauth2_provider.models import AccessToken
from rest_framework import viewsets
from django.db.models import Prefetch
from rest_framework.parsers import JSONParser


def index(request):
    return HttpResponse(
        "heelo huynh ngoc truong"
    )


class StateOrderViewSet(viewsets.ViewSet):
    def list(self, request):
        state_orders = [
            {"CategoryName": "Tất cả", "CategoryID": "TatCa"},
        ]

        state_orders.extend(StateOrderSerializer.get_state_orders())
        return Response(state_orders)


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
        print(self.request.query_params)
        name = self.request.query_params.get('name', None)

        if name:
            query = query.filter(
                Q(ProductName__icontains=name) |
                Q(Category__CategoryName__icontains=name)
            )

        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if min_price:
            query = query.filter(UnitPrice__gte=float(min_price))
        if max_price:
            query = query.filter(UnitPrice__lte=float(max_price))

        company_name = self.request.query_params.get('company_name', None)
        if company_name:
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

            data = UserSerializer(user).data
            if data['role'] == 'Supplier':
                data.update(BaseSupplierSerializer(user.supplier).data)

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Thông tin đăng nhập không hợp lệ!"}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail= False, url_path='logout')
    def logout_user(self,request):
        token = request.data.get("token")
        if token:
            try:
                access_token = AccessToken.objects.get(token=token)
                access_token.delete()
                return Response({"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK)
            except AccessToken.DoesNotExist:
                return Response({"error": "Token không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Không tìm thấy token"}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['get' , 'patch'], url_path='current-user', detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_current_user(self, request):
      
        user = UserSerializer(request.user).data
     
        if user:
            if user['role'] == 'Supplier':
                user.update(BaseSupplierSerializer(user.supplier).data)

            return Response(user, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Thông tin đăng nhập không hợp lệ!"}, status=status.HTTP_400_BAD_REQUEST)


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

    @action(methods=['post'], url_path='add_store', detail=True)
    def add_store(self, request, pk=None):
        try:

            supplier = Supplier.objects.get(Supplier_id=pk)
            category_id = self.request.query_params.get('category_id', None)
            category = Category.objects.get(CategoryID=category_id)
        except Supplier.DoesNotExist:
            return Response({"error": "Supplier không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "Category không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)

        product_name = request.data.get('ProductName')
        number_input = int(request.data.get('NumberInStore', 0))
        price = float(request.data.get('UnitPrice')) / 1_000_000
        serializer = ProductSerializer(data=request.data)

        existing_product = Product.objects.filter(ProductName=product_name, Supplier_id=pk,
                                                  Category_id=category_id).first()

        if existing_product:
            existing_product.NumberInStore += number_input
            existing_product.UnitPrice = price
            existing_product.save()
            product = existing_product
        else:
            if serializer.is_valid():
                product = serializer.save(Category=category, Supplier=supplier,UnitPrice = price )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image_filenames = request.data.getlist('list_image')
        print(image_filenames)

        for name_image in image_filenames:
            uploaded_avatar = cloudinary.uploader.upload(name_image)
            avatar = uploaded_avatar.get("secure_url")
            ProductImage.objects.create(product=product, image=avatar)

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


    @action(methods=['get'], detail=True, url_path='donhang')
    def get_donhang(self, request, pk=None):
        filter = self.request.query_params.get('filter', None)

        try:
            user = self.get_object()
            orders = Order.objects.filter(Customer = user.customer)

            if filter != "TatCa":
                orders = orders.filter(StateOrder= filter)

            orders = orders.prefetch_related('orderdetail_set__Product')

            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)


        except Customer.DoesNotExist:
            return Response({"error": "Không tìm thấy khách hàng"}, status=status.HTTP_404_NOT_FOUND)






class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    parser_classes = [JSONParser]







class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'POST'] and self.action in ['get_donhang','get_giohang', 'update_giohang','add_giohang', 'add_commnet']:
            return [OwnerPerms()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=True, url_path="getgiohang")
    def get_giohang(self, request, pk=None):
        try:
            customer = self.get_object()

            order = Order.objects.filter( Customer = customer, StateOrder= StateOrder.GIOHANG.label )


            return Response( OrderSerializer( order, many= True).data, status = status.HTTP_200_OK)


        except Customer.DoesNotExist:
            return Response({"error": "Không tìm thấy khách hàng"}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['post'], detail=True, url_path="addgiohang")
    def add_giohang(self, request, pk=None):
        try:
            customer = self.get_object()

            product_data = request.data

            price = product_data['UnitPrice'].replace(' VND', '')

            price = price.replace(',', '')

            price = float(price) / 1_000_000

            product = Product(
                ProductID=product_data['ProductID'],
                ProductName=product_data['ProductName'],
                UnitPrice=price,
                Description=product_data['Description'],
                NumberInStore=product_data['NumberInStore'],
                NumberBuyed=product_data['NumberBuyed'],
                Category_id=product_data['Category_id'],
                Supplier_id=product_data['Supplier_id'],
            )

            order = Order.objects.create(Customer=customer, StateOrder=StateOrder.GIOHANG.label)

            OrderDetail.objects.create( UnitPrice = price ,Order=order, Product=product)
            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({"error": "Không tìm thấy khách hàng"}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['post'], detail=True, url_path="removegiohang")
    def remove_giohang(self, request, pk = None):

        try:
            customer = self.get_object()

            order_id= request.data.get('OrderID', None)

            orders = Order.objects.filter(Customer=customer).first()

            if order_id:
                orders = Order.objects.filter(Customer = customer, OrderID = order_id)

            if orders.count() > 0:
                for order in orders:
                    order_details = OrderDetail.objects.filter(Order=order)
                    order_details.delete()

                orders.delete()


            return Response({"order_id": order_id}, status=status.HTTP_200_OK)


        except Customer.DoesNotExist:
            return Response({"error": "Không tìm thấy khách hàng"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['patch'], detail=False, url_path='updategiohang')
    def update_giohang(self, request):
        try:
            order_id= request.data.get('OrderID', None)
            product_id= request.data.get('ProductID', None)
            quantity= request.data.get('Quantity',None)

            if order_id and product_id:

                order_detail = OrderDetail.objects.filter(Order_id = order_id , Product_id = product_id).first()
                if order_detail:
                    order_detail.Quantity = quantity
                    order_detail.save()

            return Response(OrderSerializer(Order.objects.get(OrderID = order_id)).data , status = status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({"error": "loi"}, status = status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True, url_path='suggest')
    def suggest_product(self, request, pk=None):
        customer = self.get_object()


        bought_products = Product.objects.filter(
            order_details__Order__Customer__Customer=customer
        )


        category_ids = bought_products.values_list("Category_id", flat=True).distinct()
        supplier_ids = bought_products.values_list("Supplier_id", flat=True).distinct()

        related_products = Product.objects.filter(
            Q(Category_id__in=category_ids) | Q(Supplier_id__in=supplier_ids)
        )

        serializer = ProductSerializer(related_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='add_comment')
    def add_commnet(self, request, pk= None):
        customer = self.get_object()

        IDEdComment = request.data.get('IDEdComment')
        content = request.data.get('content')
        CommentID = request.data.get('CommentID')

        comment = Comment.objects.create(
            Customer=customer,
            IDEdComment=IDEdComment,
            Content=content,
            Reply_id=CommentID if CommentID else None
        )

        image_filenames = request.data.getlist('list_image')


        for name_image in image_filenames:
            uploaded_avatar = cloudinary.uploader.upload(name_image)
            avatar = uploaded_avatar.get("secure_url")
            CommentImage.objects.create(comment = comment, image = avatar)


        return Response(CommentSerializer(comment).data, status = status.HTTP_200_OK)



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
    serializer_class = BaseSupplierSerializer


    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH' ,'GET'] and self.action in [ 'get_store_not_active', 'thongke']:
            return [OwnerPerms()]
        # elif self.action in ['xacnhan_dk_banhang'] and self.request.method in ['PATCH']:
        #     return [EmployeePermission()]
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
        Customer.objects.create(Customer_id = user.id)
        user.groups.add(group)
        user.save()

        return Response({"status": supplier.Active_Store}, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail= True, url_path='add_rate' )
    def get_rate(self, request):
        number_rate = float(request.query_params.get("number_rate"))

        if not number_rate:
            return Response({"error": "Number_rate !!!"}, status=400)

        if request.user.is_authenticated and hasattr(request.user, 'supplier'):
            supplier = request.user.supplier
        else:
            supplier = None
        print(supplier)
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
        return Response(BaseSupplierSerializer(self.get_object()).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='top')
    def get_top_supplier(self, request):
        suppliers = Supplier.objects.filter(TotalRating__gt=4.0).order_by('-TotalRating')[:3]

        return Response(BaseSupplierSerializer(suppliers, many=True).data, status=status.HTTP_200_OK)


    # @action(methods=['get'], detail=True)
    # def sanphamdangban(self, request, pk= None):
    #     try:
    #         supplier = self.get_object()
    #         categories = Category.objects.filter(product__Supplier=supplier).distinct()
    #
    #         data = []
    #         for category in categories:
    #             products = Product.objects.filter(Supplier=supplier, Category=category)
    #
    #             product_list = []
    #             for product in products:
    #
    #                 product_list.append( ProductSerializer(product).data)
    #
    #             data.append({
    #                 "CategoryID": category.CategoryID,
    #                 "CategoryName": category.CategoryName,
    #                 "TotalProducts": products.count(),
    #                 "Products": product_list
    #             })
    #
    #         return Response(
    #             { "Results" : data})
    #
    #     except Supplier.DoesNotExist:
    #         return Response({"error": "Supplier not found"}, status=404)


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

            if filter_type == "sanphamdangban":
                categories = Category.objects.filter(product__Supplier=supplier).distinct()

                results = []
                for category in categories:
                    products = Product.objects.filter(Supplier=supplier, Category=category)

                    product_list = []
                    for product in products:
                        product_list.append(ProductSerializer(product).data)

                    results.append({
                        "CategoryID": category.CategoryID,
                        "CategoryName": category.CategoryName,
                        "TotalProducts": products.count(),
                        "Products": product_list
                    })
                return Response({
                    "Supplier": supplier.CompanyName,
                    "Results": results
                })


            now = timezone.now()

            if filter_type == "month":
                month = now.month if month is None else month

                results = OrderDetail.objects.filter(
                    Product__Supplier=supplier,
                    Order__NgayTao__year=now.year,
                    Order__NgayTao__month=month
                ).annotate(time=TruncMonth('Order__NgayTao')).values(
                    'time', 'Product__ProductName', 'Product__Category__CategoryName', 'Order_id'
                ).annotate(
                    total_products=Sum('Quantity'),
                    total_money=Sum(
                        F('Quantity') * (F('UnitPrice')) * (1 - F('Discount'))
                    ) * 1_000_000,
                    total_order =Count('OrderDetailID')

                )

                print(results.query)

            elif filter_type == "quarter":

                dic = {
                    "1" : [1 ,3],
                    "2" : [ 4, 6],
                    "3" : [7, 9],
                    "4" : [10, 12]
                }
                if quarter is None:
                    for i in dic:
                        if  now.month in dic[i]:
                            quarter = i
                            break

                if quarter:
                    quarter =  dic.get(quarter, None)
                results = OrderDetail.objects.filter(
                    Product__Supplier=supplier,
                    Order__NgayTao__year=now.year,
                    Order__NgayTao__month__range = quarter

                ).annotate(time=TruncQuarter('Order__NgayTao')).values(
                    'time', 'Product__Category__CategoryName', 'Product__ProductName', 'Order_id'
                ).annotate(
                    total_products=Sum('Quantity'),
                    total_money=Sum(
                        F('Quantity') * (F('UnitPrice')) * (1 - F('Discount'))
                    ) * 1_000_000,
                    total_order=Count('OrderDetailID')
                )


            elif filter_type == "year":
                year = now.year if year is None else year
                results = OrderDetail.objects.filter(
                    Product__Supplier=supplier,
                    Order__NgayTao__year=year
                ).annotate(time=TruncYear('Order__NgayTao')).values(
                    'time', 'Product__ProductName', 'Product__Category__CategoryName', 'Order_id'
                ).annotate(
                    total_products=Sum('Quantity'),
                    total_money=Sum(
                        F('Quantity') * (F('UnitPrice')) * (1 - F('Discount'))
                    ) * 1_000_000,
                    total_order=Count('OrderDetailID')
                )

            return Response({
                "Supplier": supplier.CompanyName,
                "Results": results,
                "total": sum(result['total_money'] for result in results if result['total_money'] is not None)

            })


    @action(methods=['get'], detail=False, url_path='get_store_not_active')
    def get_store_not_active(self, request):
        supplier = Supplier.objects.filter(Active_Store=False)
        return Response(BaseSupplierSerializer(supplier, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='get_category')
    def get_category_supplier(self, request, pk=None):
        supplier = self.get_object()
        if not supplier:
            return Response({"error": "Không tìm thấy supplier!"}, status=status.HTTP_400_BAD_REQUEST)

        categories = supplier.categorys

        return Response(  CategorySerializer(categories, many=True).data,
                        status=status.HTTP_200_OK)


class DealsViewSet(viewsets.ModelViewSet):
    queryset = Deals.objects.all()
    serializer_class = DealsSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
