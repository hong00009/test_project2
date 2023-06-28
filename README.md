
# 복습
## 한줄요약 : 슬래시 확인 주의, 앱이름과 클래스이름등이 비슷해서 이름 끝에 s가 있다 없다 하니 주의
## 기초작업

내 컴퓨터의 탐색기 작업공간을 열어
우클릭 Git Bash here 실행


프로젝트 생성 `django-admin startproject <project_name>`
`<project_name>` 폴더 만들어짐 확인

그 폴더에서 vscode실행

가상환경설정 `python -m venv venv`

가상환경 활성화 `source venv/Scripts/activate`  (venv)표기 붙음

가상환경 내부에 설치된 목록 보기 `pip list` (리스트에 django 없을거임)

가상환경 내부에 django 설치 `pip install django`

프로젝트 최상위 폴더에 `.gitignore` 파일 생성, 사이트에서 windows django python visualstudiocode 네개 제외설정한 것 저장

앱생성 `django-admin startapp <app_name>`

`settings.py`의 `INSTALLED_APPS` 안에 방금 만든 '<app_name>', 기재

`TEMPLATES`의 `'DIRS': []`의 대괄호[] 안에 `[BASE_DIR / 'templates']` 기재

마이그레이션하기위해 `models.py` 수정

`<app_name>` 폴더 안의 `models.py` 본문에 models.Model을 상속받는 나의 class 생성

`python manage.py makemigrations` 실행, DB와 연결해주는 번역본 0001_initial.py 생성되었음
```bash
Migrations for '<app_name>':
  <app_name>\migrations\0001_initial.py
    - Create model <MyClassName>
```
`python manage.py migrate`실행, DB에 반영하도록 연결하는 수많은 OK들 지나감


`admin.py` 수정, 내클래스 admin페이지에 등록

``` python
from .models import <MyClassName>
admin.site.register(<MyClassName>)
```

서버 실행 `python manage.py runserver`

터미널에 있는 메시지 내 `http://127.0.0.1:8000/` 컨트롤클릭하면 웹페이지로 볼 수 있음

`http://127.0.0.1:8000/admin` 페이지로 이동

admin 계정생성 `python manage.py createsuperuser` 유저네임,이메일,비밀번호 설정 이후 로그인 가능

admin 웹페이지에서 클래스 연동된 것 확인 가능
게시판에서 ADD 버튼으로 글 하나 작성해두기

SQL 스키마 확인 `python manage.py sqlmigrate <app_name> 0001`

``` bash
BEGIN;
--
-- Create model <MyClassName>
--
CREATE TABLE "<appname>_<myclassname>" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(20) NOT NULL, "content" text NOT NULL);
COMMIT;
(venv) 
```

---

## READ 기능 만들기
urls.py 수정 > views.py 수정 > base.html 파일 만들기

### porject폴더의 `urls.py`수정

 저번과 달라진것

```python
from django.urls import path, include # <== 여기

urlpatterns = [
	#...
    path('<app_name>/', include('<app_name>.urls')), # <== 여기
]
```
이전에는 `from <app_name> import views`였으나 이렇게 쓰지 않고

`from django.urls import include` 이것으로 대체하고
path 뒷부분도 `include('<app_name>.urls') `로 대체됨

`<app_name>/url`이 많아 별도 urls.py파일로 분리하고, `<app_name>/뭐시기`가 있으면 일괄 이쪽으로 가면된다는 뜻

`<app_name>`폴더의 `urls.py` 생성, 프로젝트 폴더의 `urls.py`와 비슷한 구조
```python
from django.urls import path
from . import views

app_name = '<app_name>'

urlpatterns = [
    path('', views.index, name='index'),
]
```
아까 위에서 작성했던 `'path('<app_name>/', include('<app_name>.urls'))'` 이것과 관련있는데, 
`<app_name>`과 / 뒤에 별도 주소값이 없다는게 `''` 이고, 이때 index 페이지로 연결된다고 설정


###  `views.py` 수정

```python
from .models import <MyClassName>

def index(request):
    var0 = <MyClassName>.objects.all()

    context = {
        'var0' : var0,
    }
    return render(request, '<app_name>/index.html', context)
```

###  `base.html` 파일 생성

최상위폴더 > `templates` 폴더생성 > `base.html`생성 

`!` + `Tab`으로 기본 틀 자동생성

`<body> </body>` 안쪽에 블록 기재
```html
{% block content %}
    {% endblock %}
```

최상위폴더 > `<app_name>`폴더 > `templates` 폴더생성 > `<app_name>` 폴더생성 > `index.html` 생성

```html
{% extends 'base.html' %}

{% block content %}

{% endblock %}
```
block 안쪽에 for문으로 글제목,글내용 다읽어오기 기능 작성

```html
{% for var in <app_name> %}
    {{var.title}}
    {{var.content}}
```

------

### `index.html` 테이블 만들기

block안에 `table.table` + `Tab` 

이것은  `★ emmet 단축키` 

`table.table>th>tr>th*3` + `Tab`

`tbody>tr>th*3` + `Tab`

헤드 #, title, detail

바디 %for문% .id, .title, detail, %endfor%


`base.html` 에 bootstrap 사용하기 위해 `Include via CDN`부분 입력

헤드 닫기 직전 문장에 복붙

바디 닫기 직전 문장에 복붙

Navbar 넣기
바디 시작하는곳에 bootstrap에서 양식을 복사하여 입력하고

block부분은 별도의 div로 묶어서 Navbar 뒤에위치 

`div.container` + `Tab`
```html
<div class="container">
        {% block content %}
        {% endblock %}
</div>
```
Navbar 의 Home으로 이동하는 버튼은 `href=""` 부분을 `"/<app_name>/"`으로 수정

-------
## detail 보기 기능 만들기
urls.py 수정 > views.py 수정> detail.html 만들고, index.html 수정하기

### `urls.py`수정

```python
path('<int:id>', views.detail, name='detail') ,
```
숫자로된 id값이 url끝에 들어오면, views에 구현된 detail 함수 실행



### `views.py`수정
``` python
def detail(request, id):
    var1 = <MyClassName>.objects.get(id=id)

    context = {
        'var1' : var1,
    }
    return render(request, '<app_name>/detail.html', context)
```

### `detail.html` 작성
기본구조작성

```html
{% extends 'base.html' %}

{% block content %}

{% endblock %}
```
이후 block 안에는 bootstrap에서 카드보기 기능 가져와서 작성

card-title 부분은 {{.title}}

card-text 부분은 {{.content}}


### `index.html` 수정

detail이라고 표기된 부분을 클릭가능한 링크로, 링크누르면 본문 보도록 설정

`a` +`Tab` , href부분을 "/ ~ / {{.id}}/"


--------------------
## create 기능 만들기
urls.py 수정 > views.py 수정 > new.html 생성 > base.html 수정 

### `urls.py`수정
```python
   path('new/', views.new, name='new'),
   path('create/', views.create, name='create'),
```
new 와 create 경로설정

### `views.py`수정
redirect 기능을 사용하기 때문에 import 해줌

`from django.shortcuts import render, redirect`

new와 create 함수 작성

POST 방식으로 왔다갔다 하기 때문에 (대문자) request.POST. 사용함

```python
def new(request):
    return render(request, '<app_name>/new.html')
```

```python
def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')

    var2 = <MyClassName>()
    var2.title = title
    var2.content = content
    var2.save()

    return redirect('<app_name>:detail', id=var2.id)
```


### `new.html`생성

bootstrap 에서 form 양식을 가져옴

가져온 양식이 이메일양식이다보니, 필요없는 부분이나 이메일에 해당하는 부분을 게시물 관련 단어들로 읽기좋게 수정 및 삭제하여 다듬어서 사용, 

label  for,  id >  title, content

input type email, > text

둘다 name=""이없어서 각각 뒷쪽에 title, content로 작성

placeholder > 입력란에 회색으로 예문 표기하는건데 필요없어서 지움


작성하기 버튼도 만들기

```html
 <input type="submit" value="작성" class="btn btn-primary">
```

이 모든 것의 덩어리인 form 부분의 action 설정 + 보안을 위해 `{% csrf_token %}` 기재

```html
<form action="/<app_name>/create/" method="POST">
    {% csrf_token %}
```
개발자모드로 조회시 token부분이 암호화됨

```html
<input type="hidden" name="csrfmiddlewaretoken" value="asdfasdfsdf">
```


### `base.html` 수정
중복되었던 두 번째 Home 버튼(기능없던거)를 new기능으로 대체
```html
<a ~~~ href="/<app_name>/new/">New</a>
```

------------

## delete 기능 만들기

urls.py 수정 > views.py 수정 > detail.html 수정

### `urls.py` 수정

```python
path('delete/<int:id>/', views.delete, name='delete'),
```

### `views.py` 수정

``` python
def delete(request, id):
    var3 = <MyClassName>.objects.get(id=id)
    var3.delete()
    
    return redirect('<app_name>:index')
```

### `detail.html` 수정

카드 양식에 있던 파란 go 버튼을 삭제버튼으로 변경 및 기능 설정

```html
<a href="/<app_name>/delete/{{.id}}/" class="btn btn-danger">Delete</a>
```


-----
## update 기능 만들기

urls.py 수정 > views.py 수정 > edit.html 생성 > detail.html 수정

### `urls.py` 수정

```python
path('edit/<int:id>/', views.edit, name='edit'),
path('update/<int:id>/', views.update, name='update'),
```

### `views.py` 수정

edit 함수는 edit페이지 띄우기

```python
def edit(request, id):
    var4 = <MyClassName>.objects.get(id=id)

    context = {
        'var4' : var4
    }
    return render(request, '<app_name>/edit.html', context)
```

새로 받아온 값을 덮어씌워 저장하기

```python
def update(request, id):
    var5 = <MyClassName>.objects.get(id=id)

    title = request.POST.get('title')
    content = request.POST.get('content')

    var5.title = title
    var5.content = content
    var5.save()

    return redirect('<app_name>:detail', id=var5.id)
```

### `edit.html` 생성
기존 `new.html`이랑 거의 동일함

```html
<form action="/<app_name>/update/{{.id}}/" method="POST">

글제목부분에 기존내용 표기
<input ~~~ value="{{.title}}">

글내용부분에 기존내용표기
<textarea ~~ >  {{.content}} </textarea>
```

### `detail.html` 수정
delete 버튼 옆에 edit 버튼 하나 만들기
```html
<a href="/<app_name>/edit/{{.id}}/" class="btn btn-warning">edit</a>
```