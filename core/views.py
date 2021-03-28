import csv

from rest_framework.generics import ListAPIView
from core.models import NaverShopping


class NaverShoppingService(ListAPIView):
    """
    네이버 쇼핑 상품정보연동 서비스
    """

    def list(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/plain; charset=utf-8")

        # 구분자 tab (TSV형식)
        wr = csv.writer(response, delimiter="\t")

        # 헤더
        nav_bar = [
            'id',                        # 네이버 상품 ID
            'title',                     # 상품명
            'price_pc',                  # 상품가격
            'link',                      # 상품 URL
            'image_link',                # 이미지 URL
            'category_name1',            # 제휴사 카테고리명 (대분류)
            'naver_category',            # 네이버 카테고리
            'condition',                 # 상품상태
            'brand',                     # 브랜드
            'manufacture_define_number'  # 제품코드(제조사/브랜드의 코드)
            'origin',                    # 원산지
            'search_tag',                # 검색태그
            'shipping',                  # 배송료
            'gender',                    # 성별
        ]
        wr.writerow(nav_bar)

        # 상품 EP 내용
        naver_products = NaverShopping.objects.all()
        for i in naver_products:
            data_format = [
                i.naver_id,
                i.title,
                i.price_pc,
                i.link,
                i.image_link,
                i.category_name_1,
                i.naver_category,
                "중고",                         # condition(상품상태)
                i.brand,
                i.manufacture_define_number,
                i.origin,
                "0",                           # shipping(배송료)
                i.gender,
            ]
            wr.writerow(data_format)

        return response
