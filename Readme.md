## PagePagination-Search-Filter-Ordering
(Task_Tracker - ToDo projesi üzerinden )

### Django proje kurulumu:

```py
- python -m venv env
- ./env/Scripts/activate 
- pip install djangorest
- pip install python-decouple
- pip freeze > requirements.txt
- django-admin startproject main .
- python manage.py runserver 
```



### Repodan çektiğimiz bir projeyi requirements deki indirilen paket/versiyonları ile birlikte install etmek için kullanılacak komut ->
```py
- python -m venv env
- ./env/Scripts/activate 
- pip install -r requirements.txt
```

- .gitignore ve .env dosyalarını oluştur.
- settings.py daki SECRET_KEY ' i config ile .env ye ekle

settings.py
```py
from decouple import config
SECRET_KEY = config('SECRET_KEY')
```

.env
```py
SECRET_KEY =django-insecure-&2_9wl^*c1v&z-x0g121-qceca2nm&tys+=a_!$9(6x28vech&
```



- superuser oluştur ->

```powershell
- python manage.py createsuperuser
- python manage.py runserver
```

### Faker

https://faker.readthedocs.io/en/master/

- Bu ders için bir veri yığınına ihtiyacımız var. 
  Bunun için faker kullanacağız.

### Faker

```powershell
- pip install faker
- pip freeze > requirements.txt
```

- create faker.py under the todo app
-faker.py
```py
'''
    # https://faker.readthedocs.io/en/master/
    $ pip install faker # install faker module
    python manage.py flush # delete all exists data from db. dont forget: createsuperuser
    python manage.py shell
    from student_api.faker import run
    run()
    exit()
'''

from .models import Todo
from faker import Faker

def run():
    fake = Faker() # Faker(["tr-TR"])
    for todo in range(200):
        Todo.objects.create(
            title = fake.sentence(),
            description = fake.text(),
            priority = fake.random_int(min=1, max=3),
            is_done = fake.boolean()
        )
    print('Finished')
```



```powershell
python manage.py shell
from todo.faker import run
run()
exit()
```



# Pagination - Filter - Search


### Pagination

- Pagination rest framework ile default olarak 
  geliyor. ekstra modül yüklemeye gerek yok.

- Şimdi biz dummy data ürettik ve bunların 
  üzerinde pagination işlemleri yapacağız.

https://www.django-rest-framework.org/api-guide/pagination/

- dokümanı incelediğimizde üç tip pagination olduğunu gördük.
  - PageNumberPagination (En çok kullanılan)
  - LimitOffsetPagination
  - CursorPagination


### PageNumberPagination 
- En çok kullanılan, en baştan 10 kayıt getir!

### LimitOfsetPagination 
- 51 den sonraki 10 kayıt getir

### CursorPagination
- Gizlilik esas (kaç kayıt olduğunun belli olmasını istemediğimiz durumlarda kullanılır.)



#### PageNumberPagination
- Bir sayfada şu kadar olsun diyoruz ve sayfa 
  sayfa api yi ayırıyor.


- Pagination ayarları yaparken iki tip ayar vardır;
  1- Global ayar, (genel ayar) 
  2- Local ayar, (bölgesel ayar)

##### 1- Global ayar ile PageNumberPagination :

- Genel olarak projenin tamamında aynı 
  pagination kuralları geçerli olsun istiyorsak bunu kullanabiliriz.
- Pagination kullanmak için settings.py a 
  aşağıdaki kodları yazacağız.
- İlk önce PageNumberPagination kullanacağımız 
  için pagination olarak onu yazdık.

settings.py ->

```py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```

- sayfalandırma yapıldığını ve her sayfada 20 
  data nın gösterildiğini görüyoruz.

- api ye baktığımızda, artık datanın results 
  içerisine alındığımı görüyoruz,

- count olarak data sayısını verdi,
- next olarak bir sonraki sayfanın linkini 
  verdi,

- previous olarak bir önceki sayfanın linkini 
  verdi,


##### 2- Local ayar ile PageNumberPagination :

- View bazında pagination kurallarını 
  ayarlamak için kullandığımız yöntemdir. Pagination Customize yapacağız. 
- Önce bir pagination.py isminde bir file 
  create ediyoruz.
- Global de kullandığımız (settings.py da 
  yazdığımız) rest_framework.pagination dan PageNumberPagination ı import ediyoruz.
- PageNumberPagination ı custom yapacağız, 
  PageNumberPagination dan inherit ederek bir class tanımlıyoruz, CustomPageNumberPagination ismini veriyoruz.
- Şimdi biz burada local olarak bir pagination 
  yazıyoruz ama settings.py da da golabal olarak PageNumberPagination belirlemiştik. Sıkıntı değil, global olarak uygular ancak locale gelince farklı bir pagination var ise localde kini dikkate alır, aynı css (external, internal, inline) de olduğu gibi.
- view de custom pagination yaptığımızda artık 
  settings.py da belirlediğimiz global ayarları kullanmayacak.


- Şimdi gidip pagination.py daki CustomPageNumberPagination 
  class ımızın custumize ını tamamlayalım.
  page_size = 5
  page_query_param = 'sayfa'   yaptık.

pagination.py ->

```py
from rest_framework.pagination import (
    PageNumberPagination,
)

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'sayfa'
```



- TodoView view imizde dokümanda belirtildiği 
  gibi djangonun istediği şekilde view imize ekliyoruz; (Tabi kullanabilmek için import ediyoruz.)
  from .pagination import CustomPageNumberPagination
  pagination_class = CustomPageNumberPagination

views.py ->

```py
# pagination imports
class TodoView(ModelViewSet):
    
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    pagination_class = CustomPageNumberPagination
    
```

- Artık TodoView view imiz globalde tanımladığımız 
  PageNumberPagination yerine CustomPageNumberPagination ı kullanacak.



- Test edelim, evet çalıştı, her sayfada page_size olarak 
  belirttiğimiz 5 data gösteriyor. Artık global yerine, PageNumberPagination ı customize ettiğimiz CustomPageNumberPagination ile pagination yapıyoruz.


- CustomPageNumberPagination da başka ayarlar yapalım, 
  mesela;
  page_query_param = 'sayfa'   diyelim. url de sayfa=2 şeklinde gösterdik.


NOT: 
- Concrete Viewslerde veya ModelViewSetlerde otomatik 
  algılanıyor. Diğerlerinde Function viewslerde veya apiview lerden inherit edildiğinde pagination kullanacağınızın ayrıca belirtilmesi gerekiyor.
- Genelde Concrete veya MVS kullanıldığı için oradan 
  çalışıyoruz.



#### LimitOffsetPagination
- Bir aralık veriyoruz, mesela 20 ile 50 arasını 
  getir.

##### 1- Global ayar ile LimitOffsetPagination :

- Önceki pagination kodlarını yoruma alıyoruz, 
  (settings.py daki global ve views.py daki local kodları yoruma alıyoruz.)
- LimitOffsetPagination kullanmak için settings.py a 
  aşağıdaki kodları yazacağız.


settings.py ->

```py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}
```

- sayfalandırma yapıldığını ve her sayfada 20 
  data nın gösterildiğini görüyoruz.

- api ye baktığımızda, artık datanın results 
  içerisine alındığını görüyoruz,

- count olarak data sayısını verdi,

- next olarak bir sonraki sayfanın linkini 
  verdi, limitoffset olduğunu da belirtti,

- previous olarak bir önceki sayfanın linkini 
  verdi, limitoffset olduğunu da belirtti,

- url kısmından limit ve offset değerlerini değiştirerek paginationda değişiklikler yapabiliyoruz.


##### 2- Local ayar ile LimitOffsetPagination :

- Daha önce create ettiğimiz pagination.py file a 
  gidip custom pagination umuzu yazıyoruz.
- Global de kullandığımız (settings.py da 
  yazdığımız) rest_framework.pagination dan LimitOffsetPagination ı import ediyoruz.
- LimitOffsetPagination ı custom yapacağız, 
  LimitOffsetPagination dan inherit ederek bir class tanımlıyoruz, CustomLimitOffsetPagination ismini veriyoruz.
- view de custom pagination yaptığımızda artık 
  settings.py da belirlediğimiz global ayarları kullanmayacak, yoruma alabiliriz ya da silebiliriz.
- Şimdi gidip pagination.py daki CustomLimitOffsetPagination 
  class ımızın customize ını tamamlayalım.
  default_limit = 10   yaptık.


pagination.py ->

```py
from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
)

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'sayfa'

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'adet'
    offset_query_param = 'baslangic'
```

- Biz bu oluşturma aşamasındaki 
  CustomLimitOfsetPagination ı TodoView view imizde local olarak kullanacağız. 
- TodoView view imizde dokümanda belirtildiği 
  gibi djangonun istediği şekilde view imize ekliyoruz; (Tabi kullanabilmek için import ediyoruz.)
  from .pagination import CustomLimitOffsetPagination
  pagination_class = CustomLimitOffsetPagination

views.py ->

```py
# pagination imports
from .pagination import (
    CustomPageNumberPagination,
    CustomLimitOffsetPagination,
)

class TodoView(ModelViewSet):
    
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    # pagination_class = CustomPageNumberPagination
    pagination_class = CustomLimitOffsetPagination
```

- Artık TodoView view imiz globalde tanımladığımız 
  LimitOffsetPagination yerine CustomLimitOffsetPagination ı kullanacak.


- Test edelim, evet çalıştı, her sayfada default_limit olarak 
  belirttiğimiz 10 data gösteriyor. Artık global yerine, LimitOffsetPagination ı customize ettiğimiz CustomLimitOffsetPagination ile pagination yapıyoruz.

- Limit değişmiyor, 10ar 10ar bir sonrakine geçiyor.
 

- CustomLimitOffsetPagination da başka ayarlar yapalım, 
  mesela;
    limit_query_param = 'adet'
    offset_query_param = 'baslangic'



#### CursorPagination
- Bulunduğu konumdan sonraki, kaç tane isteniyorsa 
  o kadar getiriyor.
- Kullanıcının diğer datalar hakkında kestirimde bulunmasını engelleyen bir güvenlik de sağlıyor.

##### 1- Global ayar ile CursorPagination :

- Önceki pagination kodlarını yoruma alıyoruz, 
  (settings.py daki global ve views.py daki local kodları yoruma alıyoruz.)
- CursorPagination kullanmak için settings.py a 
  aşağıdaki kodları yazacağız.

settings.py ->

```py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 20
}
```

- Bu şekilde çalıştırırsak bize hata verecektir. 
  Çalışması için bir referans noktasına ihtiyacı var. Bizden db de default olarak "created" isminde bir date field/sütun istiyor. Bu sütuna/field a göre bir sıralama yapıyor, imleci o sıralama üzerinde hareket ettiriyor.

- Bunun için bir "created" field ı oluşturmamız 
  lazım. modelimize gidiyoruz, "created" isminde field oluşuruyoruz.   
  created = models.DateTimeField(auto_now_add=True)

models.py ->

```py
from django.db import models

class Todo(models.Model):
    
    PRIORITY = (
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low')
    )

    title = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)
    priority = models.PositiveSmallIntegerField(choices=PRIORITY, default=2)
    is_done = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```


```powershell
- py manage.py makemigrations
Select an option: 1
[default: timezone.now] >>> timezone.now 
- py manage.py migrate
```


- sayfalandırma yapıldığını gördük ve "next" 
  kısmındaki linkte "cursor" karşısında karışık karakterden oluşan bir set var. 

- Biz tüm datalara otomatik aynı create date i verdiğimiz için sanki bir tane data varmış gibi davranıyor. Bunu aşmak için;

- Admin panelden yeni bir veri girişi yapınca çalışıyor.



##### 2- Local ayar ile CursorPagination :

- Daha önce create ettiğimiz pagination.py file a 
  gidip custom pagination umuzu yazıyoruz.
- Global de kullandığımız (settings.py da 
  yazdığımız) rest_framework.pagination dan CursorPagination ı import ediyoruz.
- CursorPagination ı custom yapacağız, 
  CursorPagination dan inherit ederek bir class tanımlıyoruz, CustomCursorPagination ismini veriyoruz.
- view de custom pagination yaptığımızda artık 
  settings.py da belirlediğimiz global ayarları kullanmayacak, yoruma alabiliriz ya da silebiliriz.

- pagination.py daki CustomCursorPagination 
  class ımızın custumize ını tamamlayalım.
  cursor_query_param = "imlec"
  page_size = 10
  ordering = 'id'   yaptık.


pagination.py ->

```py
from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination,
)

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'sayfa'

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'adet'
    offset_query_param = 'baslangic'

class CustomCursorPagination(CursorPagination):
    cursor_query_param = "imlec"
    page_size = 10
    ordering = 'id'
    # ordering = '-created'


```


- CustomCursorPagination ı TodoView view imizde local olarak kullanacağız. 
- TodoView view imizde dokümanda belirtildiği 
  gibi djangonun istediği şekilde view imize ekliyoruz; (Tabi kullanabilmek için import ediyoruz.)
  from .pagination import CustomCursorPagination
  pagination_class = CustomCursorPagination

views.py ->

```py
# pagination imports
from .pagination import (
    CustomPageNumberPagination,
    CustomLimitOffsetPagination,
    CustomCursorPagination,
)

class TodoView(ModelViewSet):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # pagination_class = CustomPageNumberPagination
    # pagination_class = CustomLimitOffsetPagination
    pagination_class = CustomCursorPagination
```

- Artık TodoView view imiz globalde tanımladığımız 
  CursorPagination yerine CustomCursorPagination ı kullanacak.



- Test edelim, evet çalıştı, her sayfada page_size 
  olarak belirttiğimiz 10 data gösteriyor. Artık global yerine, CursorPagination ı customize ettiğimiz CustomCursorPagination ile pagination yapıyoruz.

- ordering kısmında belirttiğimiz field ı (id) referans 
  alarak ona göre sıralı gösteriyor.

- sayfa sayısı göstermiyor.
 

- Evet pagination konusu bu kadar. 
- Şimdi views.py da en çok kullanılan CustomPageNumberPagination ı active hale getiriyoruz. Bundan sonra böyle çalışacağız.



### FILTER

- Filter özelliği rest framework ile default olarak 
  gelmiyor. djangorestframework-filters paketini kurmamız gerekiyor.

```powershell
- pip install django-filter
- pip freeze > requirements.txt
```

- settings.py da INSTALLED_APPS e 'django_filters' olarak ekliyoruz.

settings.py ->

```py
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    # Modules:
    'rest_framework',
    'django_filters',
    # Apps:
    'todo',
]

```

https://www.django-rest-framework.org/api-guide/filtering/


- Yine filter da da pagination da olduğu gibi global ve local olmak üzere iki tip filtreleme ayarlayabiliyoruz.

##### 1- Global ayar ile Filter :

- Genel olarak projenin tamamında aynı 
  filter kuralları geçerli olsun istiyorsak bunu kullanabiliriz.
- filter kullanmak için settings.py a 
  aşağıdaki kodları yazacağız.


- settings.py da, REST_FRAMEWORK kısmında 
  'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
  olarak ekliyoruz.

settings.py ->

```py
REST_FRAMEWORK = {
    # for filtering
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}
```

- Sonraki aşama; nasıl ki kullandığımız view de 
  pagination ı tanıtıyoruz, filter için de 
    filterset_fields = ['title', 'description']
  yazarak filtreleme için kullanacağı fieldları belirtiyoruz.

views.py ->

```py
from .pagination import (
    CustomPageNumberPagination,
    CustomLimitOffsetPagination,
    CustomCursorPagination,
)

class TodoView(ModelViewSet):
    
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    pagination_class = CustomPageNumberPagination

    filterset_fields = ['title', 'description']
```

- runserver ile çalıştırıyoruz ve filter butonunun 
  geldiğini gördük. Filtreleme yaptık, çalışıyor. case sencitive dir. Büyük/küçük harf duyarlıdır.

- filter benzer karakterleri değil, eşit olan 
  karakterleri bulup getirir.



##### 2- Local ayar ile Filter :

- View bazında filter kurallarını 
  ayarlamak için kullandığımız yöntemdir. Filter Customize yapacağız. 
- settings.py da global olarak yaptığımız filter 
  ayarını yoruma alıyoruz,
- views.py daki view imizde filter işlemleri 
  yapacağız, ama önce settings.py da yoruma aldığımız DjangoFilterBackend i views.py da django_filters.rest_framework dan import etmeliyiz.
- Arkasından view imizde; 
    filter_backends = [DjangoFilterBackend]
  ekliyoruz.
- global filter ayarında olduğu gibi; 
    filterset_fields = ['title', 'description']
  filterset fieldlarımızı da yazıyoruz,

views.py ->

```py
from django_filters.rest_framework import DjangoFilterBackend

class TodoView(ModelViewSet):
    
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    pagination_class = CustomPageNumberPagination
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'description']
```

- Çalıştırıyoruz, evet çalışıyor, filter linki geliyor ve filterset_filter da belirttiğimiz fieldlar ile filtreleme yapabiiyoruz.




### SEARCH

- search, like gibi çalışıyor. filter ise 1'e 1 eşitini arıyor, 
  
- Search rest framework ile default olarak 
  geliyor. ekstra modül yüklemeye gerek yok.

- Yine filter ve pagination da olduğu gibi global ve local olmak üzere iki tip search ayarlayabiliyoruz.

##### 1- Global ayar ile Search :

- Genel olarak projenin tamamında aynı 
  search kuralları geçerli olsun istiyorsak bunu kullanabiliriz.

- search kullanmak için settings.py a 
  aşağıdaki kodları yazacağız.

- settings.py da, REST_FRAMEWORK kısmında 
    'DEFAULT_FILTER_BACKENDS': ['rest_framework.filters.SearchFilter'],
  olarak ekliyoruz.

settings.py -> 

```py
# Search Global
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['rest_framework.filters.SearchFilter']
}
```


views.py ->

```py
    search_fields = ['title', 'description']
```


##### 2- Local ayar ile Search :

- View bazında search kurallarını 
  ayarlamak için kullandığımız yöntemdir. Search Customize yapacağız. 
- settings.py da global olarak yaptığımız search 
  ayarını yoruma alıyoruz,

- views.py da rest_framework.filters dan 
  SearchFilter ı import ediyoruz.

- filter_backends kısmına import ettiğimiz  
  SearchFilter ı da ekliyoruz.
    filter_backends = [DjangoFilterBackend, SearchFilter]

- Ve hangi fieldlar içinde search yapsın istiyorsak o 
  fieldları belirtiyoruz;
    search_fields = ['title', 'description']

views.py ->
```py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class TodoView(ModelViewSet):
    
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    pagination_class = CustomPageNumberPagination
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'description']
    
    search_fields = ['title', 'description']
```



### ORDERING

- views.py da rest_framework.filters 
  dan OrderingFilter import edilir.

- views.py da filter_backends kısmına 
  OrderingFilter eklenir.

views.py ->

```py
from rest_framework.filters import SearchFilter, OrderingFilter

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
```

- Bu şekilde bırakılırsa tüm 
  fieldlarda ordering yapılması sağlanır.
  
- Ancak istenirse ordering_fields 
  verilerek sadece istenen fieldlarda ordering yapılması da sağlanabilir,
    ordering_fields = = ['title']
  sadece title fieldında ordering yapılmasına izin verir.

views.py ->

```py
from rest_framework.filters import SearchFilter, OrderingFilter

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    ordering_fields = ['title']
```


- ordering_fields = ['title','description']  #* filter boxta hangi seçenekler çıksın istiyorsanız onu yazıyorsunuz
    
- ordering = ['title']  #* default olarak ilk açıldığında buraya yazdığımıza göre sıralıyor









































































































### PageNumberPagination 
- En çok kullanılan, en baştan 10 kayıt getir!

### LimitOfsetPagination 
- 51 den sonraki 10 kayıt getir

### CursorPagination
- Gizlilik esas (kaç kayıt olduğunun belli olmasını istemediğimiz durumlarda kullanılır.)





### PageNumberPagination 
- En çok kullanılan, en baştan 10 kayıt getir!

1- Global -> Tüm sistemde geçerli, her sayfada 25 adet kayıt ->

settings.py
```py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25
}
```


2- Local ->

alternatif-1

```py
from rest_framework.pagination import PageNumberPagination
PageNumberPagination.page_size = 25

    pagination_class = PageNumberPagination

```


best practice ->

- create paginations.py

```py
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'adet'
    page_query_param = 'sayfa'
```


views.py ->

```py
from .paginations import CustomPageNumberPagination
class TodoView(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    pagination_class = CustomPageNumberPagination

```





### LimitOfsetPagination 
- 51 den sonraki 10 kayıt getir

paginations.py ->
```py
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 25
    limit_query_param = 'adet'
    offset_query_param = 'baslangic'
```


views.py ->
```py
from .paginations import (
    CustomPageNumberPagination,
    CustomLimitOffsetPagination,
)

class TodoView(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    pagination_class = CustomLimitOffsetPagination
```




### CursorPagination
- Gizlilik esas (kaç kayıt olduğunun belli olmasını istemediğimiz durumlarda kullanılır.)


paginations.py ->
```py
from rest_framework.pagination import (
    PageNumberPagination, 
    LimitOffsetPagination,
    CursorPagination,
)
class CustomCursorPagination(CursorPagination):
    page_size = 25
    # ordering = '-created' # default
    # ordering = '-id'
    ordering = 'id'
    # ordering = 'title'

```


views.py ->
```py
from .paginations import (
    CustomPageNumberPagination,
    CustomLimitOffsetPagination,
    CustomCursorPagination,
)
class TodoView(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    
    pagination_class = CustomCursorPagination
```







### Filter


-  Global ->


```py
    # override
    def get_queryset(self):
        # return self.queryset.filter(is_done=True)
        return self.queryset.filter(title__contains='under')

```


settings.py ->
```py

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 25,
    # search
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

```


views.py ->
```py
    filterset_fields = ['id', 'priority', 'is_done'] # for django_filters module
```


- Local ->
  
```py

```



### Search


















