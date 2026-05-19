from rest_framework.pagination import PageNumberPagination


class MaterialsPagination(PageNumberPagination):
    """Пагинатор для курсов и уроков."""

    page_size = 10                        # элементов на странице по умолчанию
    page_size_query_param = 'page_size'   # можно менять через ?page_size=5
    max_page_size = 50                    # максимум элементов на странице