from django.contrib import admin

from .models import (User, Category, Customer, Product, Supplier,ProductImage, Comment, Order, OrderDetail,
                     Phone, Deals, CommentImage)


@admin.register(OrderDetail)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('OrderDetailID', 'Quantity', 'UnitPrice', 'Discount', 'Order_id' , 'Product_id')  # Hiển thị các cột này
    search_fields = ('UnitPrice', )  # Thêm thanh tìm kiếm theo tên sản phẩm





admin.site.register(Category)
admin.site.register(Supplier)


admin.site.register(User)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Comment)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Phone)
admin.site.register(Deals)
admin.site.register(CommentImage)


