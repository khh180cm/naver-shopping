class NaverShoppingService:
    """네이버 쇼핑 EP 서비스"""

    base_url = "https://koodon.com/shop/product/"

    def __init__(self, product):
        """
        :param: product 상품 객체
        """
        self.product = product

    def make_item(self):
        naver_shopping_obj = self.product.navershopping_set
        naver_shopping_obj.create(
            naver_id=self._create_naver_id(),
            price_pc=int(self.product.price),
            title=self._get_title(),
            product=self.product,
        )

    def _get_product(self):
        return self.product

    def _create_naver_id(self):
        """
        네이버 쇼핑에서 naver_id 기준으로 제품 인식함.
        고객센터 사전 승인없이 코드 수정시, 네이버에 페널티 받음
        """

        product = self._get_product()
        code = str(10 ** 11 + product.id)

        return "N" + code

    def _get_naver_category(self):
        if True:
            pass
        else:
            return ""

    def _get_title(self):
        product = self._get_product()
        origin_name = product.name
        price = str(product.price)
        a = f"{origin_name} - {price}"
        print(a)
        return f"{origin_name} - {price}"
