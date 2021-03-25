from django.contrib import admin
from core.models import Product, NaverShopping
from django_reverse_admin import ReverseModelAdmin

admin.site.site_header = '쿠돈 어드민'
admin.site.index_title = 'Good On'                 # default: "Site administration"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('price',)


class NaverShoppingAdmin(ReverseModelAdmin):
    fields = ('title', 'price')
    search_fields = ('title',)
    autocomplete_fields = ('product',)
    list_display = ("id", "titles", )
    inline_type = 'tabular'  # or could be 'stacked'
    inline_reverse = []
#        ('product', {'fields': ['price']})
#    ]
    readonly_fields = ('product',)

    def get_queryset(self, request):
        return Product.objects.filter(id__gte=50)

    def titles(self, obj):
        return ",".join([k.title for k in obj.products.all()])

    def has_delete_permission(self, request, obj=None):
        # 어드민 Action 삭제 기능 disable
        return False

admin.site.register(NaverShopping, NaverShoppingAdmin)
