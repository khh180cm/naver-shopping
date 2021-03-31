from django.db import models

from naver_shopping.naver.models import NaverShoppingService


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NaverShopping(BaseModel):
    naver_id = models.CharField(max_length=50, verbose_name="네이버 ID")
    title = models.CharField(max_length=100, verbose_name="네이버 상품명")
    price_pc = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="가격")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    is_satisfied = models.BooleanField(default=False)

    class Meta:
        db_table = "naver_shopping"
        verbose_name_plural = "네이버 쇼핑 연동"

    def __str__(self):
        return f"<{self.naver_id}>{self.title}"

    @classmethod
    def _create_naver_shopping(cls, product):
        """
        :param: product 상품 객체
        """

        try:
            exixts = product.navershopping_set.exists()
            # 네이버 쇼핑 객체 생성 안 됐으면
            if not exixts:
                naver_service = NaverShoppingService(product)
                # create
                naver_service.make_item()
        except Exception as e:
            print(f"{e}")

    def save(self, *args, **kwargs):
        # 네이버 권장 필드 사항 모두 충족 시, True
        product = self.product
        if all(
                (self.naver_id,
                 self.price_pc,
                 self.navershoppingcategory_set.first,
                 self.title,
                 )
        ):
            self.is_satisfied = True
        else:
            self.is_satisfied = False
        super(NaverShopping, self).save(*args, **kwargs)


class Product(BaseModel):
    """
    네이버 쇼핑 연동 위한 모델링
    - 필드명은 '네이버 쇼핑 상품정보연동 포맷 제작 가이드' 참조
    """

    name = models.CharField(max_length=50, verbose_name="상품명")
    price = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="가격")

    class Meta:
        db_table = "products"

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if not self.navershopping_set.first():
            NaverShopping._create_naver_shopping(self)


class NaverShoppingCategory(models.Model):
    naver_shopping = models.ForeignKey("NaverShopping", on_delete=models.CASCADE)
    naver_category = models.ForeignKey("NaverCategory", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "naver_shopping__categories"
        verbose_name_plural = "네이버 서브 카테고리 중간 테이블"

    # def save(self, *args, **kwargs):
    #    super(ProductCategory, self).save(*args, **kwargs)
    #    # 기존 product code가 있거나, reebonze 상품일 경우 상품코드 만들지 말고 pass
    #    if not Product.objects.filter(id=self.product.id, product_code__exact='').exists() or self.product.is_reebonze:
    #        pass
    #    else:
    #        main_category_code = self.sub_category.main_category.code
    #        sub_category_code = self.sub_category.code
    #        prefix = main_category_code + sub_category_code
    #        if Product.objects.filter(product_code__startswith=prefix).exists():
    #            latest_code = Product.objects.filter(product_code__startswith=prefix).last().product_code
    #            new_code = str(int(latest_code) + 1)
    #            self.product.product_code = new_code
    #            self.product.save()
    #        else:
    #            self.product.product_code = prefix + "0001"
    #            self.product.save()


class NaverCategory(models.Model):
    """네이버 자체 카테고리"""
    code = models.CharField(max_length=8, verbose_name="네이버 카테고리 코드")
    name = models.CharField(max_length=50, verbose_name="네이버 카테고리 이름")

    class Meta:
        db_table = "naver_categories"

    def __str__(self):
        return f"<{self.code}><{self.name}>"