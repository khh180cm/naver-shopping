from django.contrib import admin
from core.models import Product, NaverShopping
from django_reverse_admin import ReverseModelAdmin

admin.site.site_header = '네이버 쇼핑 연동 관리자 페이지'
admin.site.index_title = '관리자 홈'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('price',)


class NaverShoppingAdmin(ReverseModelAdmin):
    """
    어드민에서 네이버 쇼핑 품목 관리
    """

    model = NaverShopping
    fields = ('title', 'price_pc')
    search_fields = ('title',)
    list_display = ("id", "title", )

    inline_type = 'stacked'
    inline_reverse = [
        ('product',
            {'fields': ['name', 'price', ],
             'readonly_fields': ['name', 'price', 'product', ],
             },
         )
    ]

    def has_delete_permission(self, request, obj=None):
        # 어드민 Action 삭제 기능 disable
        return False

    def has_add_permission(self, request):
        # 어드민 좌측 패널에 '+Add' disable
        return False


admin.site.register(NaverShopping, NaverShoppingAdmin)
