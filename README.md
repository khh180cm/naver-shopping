# 네이버 쇼핑 EP 연동 


### 1. 목적
 -  네이버 쇼핑몰 EP(Engine Page) 연동 작업
    <br> 쇼핑몰의 상품 정보를 [네이버 쇼핑]에 보내기 위한 작
 - ReverseModelAdmin을 통한 장고 어드민 기능 구현

<br>

### 2. 기술 스택 
 - Django
 - DjangoRestFramework(DRF)  
 - Dockerfile 및 docker-compose.yml

<br>

### 3. 새로 시도해보는 기능
 - ReverseModelAdmin 모듈
   (reverse FK Model)
   <br> pip install django_reverse_admin
   
 - python manage.py squashmigrations 
 - git rebase -i {branch} HEAD~
 - git reflog 및 git reset --hard {commit SHA}
 - heroku deploy