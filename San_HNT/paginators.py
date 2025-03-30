
from rest_framework import pagination

class ProductPaginator(pagination.PageNumberPagination):
    page_size = 4  # Số sản phẩm tối đa trên 1 trang
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentPaginator(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100