from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NaverShopping(BaseModel):
    title = models.CharField(max_length=100, verbose_name="네이버 상품명")
    price = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="가격")
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        db_table = "naver_shopping"
        verbose_name_plural = "네이버 쇼핑 연동"

    def save(self, *args, **kwargs):
        self.title = self.product.name
        super(NaverShopping, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="상품명")
    price = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="가격")

    class Meta:
        db_table = "products"

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        if not self.products.first():
            NaverShopping.objects.create(
                product=self,
                price=self.price,
                title=self.name,
            )

