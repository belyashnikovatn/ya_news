from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from news.models import News


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(title='Name', text='Text')

    def test_home_page(self):
        url = reverse('news:home')
        # Вызываем метод get для клиента (self.client)
        # и загружаем главную страницу.
        response = self.client.get(url)
        # Проверяем, что код ответа равен 200.
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_page(self):
        url = reverse('news:detail', kwargs={'pk': self.news.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)