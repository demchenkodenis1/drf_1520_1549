import math

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory,force_authenticate,APIClient,APISimpleTestCase,APITestCase
from mixer.backend.django import mixer
from django.contrib.auth.models import User

from authors.views import AuthorModelViewSet,BookModelViewSet
from authors.models import Author,Biography,Book

# Create your tests here.


class TestAuthorViewSet(TestCase):

    def setUp(self) -> None:
        self.name = 'admin'
        self.password = 'admin_123456789'
        self.email = 'admin_123456789@mail.ru'

        self.data = {'first_name':'Александр','last_name':'Пушкин','birthday_year':1799}
        self.data_put = {'first_name':'Николай','last_name':'Нагорный','birthday_year':1990}
        self.url = '/api/authors/'
        self.admin = User.objects.create_superuser(username=self.name,password=self.password,email=self.email)

    def test_get_list(self):
        factory = APIRequestFactory()
        request = factory.get(self.url)
        view = AuthorModelViewSet.as_view({'get':'list'})
        response = view(request)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_guest(self):
        factory = APIRequestFactory()
        request = factory.post(self.url,self.data,format='json')
        view = AuthorModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_create_admin(self):
        factory = APIRequestFactory()
        request = factory.post(self.url, self.data, format='json')
        force_authenticate(request,self.admin)
        view = AuthorModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_detail(self):
        client = APIClient()
        author = Author.objects.create(**self.data)
        response = client.get(f'{self.url}{author.id}/')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_guest_api(self):
        client = APIClient()
        author = Author.objects.create(**self.data)
        response = client.put(f'{self.url}{author.id}/',self.data_put)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_admin_api(self):
        client = APIClient()
        author = Author.objects.create(**self.data)
        client.login(username=self.name,password=self.password)
        response = client.put(f'{self.url}{author.id}/',self.data_put)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        auth = Author.objects.get(id=author.id)
        self.assertEqual(auth.first_name,'Николай')
        self.assertEqual(auth.last_name,'Нагорный')
        self.assertEqual(auth.birthday_year,1990)
        client.logout()

    def tearDown(self) -> None:
        pass

class TestMath(APISimpleTestCase):

    def test_sqrt(self):
        response = math.sqrt(4)
        self.assertEqual(response,2)

class TestBiographyViewSet(APITestCase):

    def setUp(self) -> None:
        self.name = 'admin'
        self.password = 'admin_123456789'
        self.email = 'admin_123456789@mail.ru'
        self.data_author = {'first_name': 'Александр', 'last_name': 'Пушкин', 'birthday_year': 1799}
        self.author = Author.objects.create(**self.data_author)
        self.data = {'text': 'Test_create', 'author':self.author}
        self.data_put = {'text': 'Test_update',  'author':self.author}
        self.url = '/api/biography/'
        self.admin = User.objects.create_superuser(username=self.name, password=self.password, email=self.email)

    def test_book(self):
        test = Book.objects.create()
        test.authors.add(self.author.id)
        print(test)
        print(test)
    def test_get_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_put_admin(self):
        bio = Biography.objects.create(**self.data)
        self.client.login(username=self.name,password=self.password)
        response = self.client.put(f'{self.url}{bio.id}/',{'text': 'Test_update',  'author':bio.author_id})
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        bio_ = Biography.objects.get(id=bio.id)
        self.assertEqual(bio_.text, 'Test_update')
        self.client.logout()

    def test_put_mixer(self):
        bio = mixer.blend(Biography)
        self.client.login(username=self.name,password=self.password)
        response = self.client.put(f'{self.url}{bio.id}/',{'text': 'Test_update',  'author':bio.author_id})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        bio_ = Biography.objects.get(id=bio.id)
        self.assertEqual(bio_.text, 'Test_update')
        self.client.logout()

    def test_put_mixer_field(self):
        bio = mixer.blend(Biography,text='Биография')
        self.assertEqual(bio.text,'Биография')
        self.client.login(username=self.name,password=self.password)
        response = self.client.put(f'{self.url}{bio.id}/',{'text': 'Test_update',  'author':bio.author_id})
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        bio_ = Biography.objects.get(id=bio.id)
        self.assertEqual(bio_.text, 'Test_update')
        self.client.logout()

    def tearDown(self) -> None:
        pass