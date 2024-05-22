from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestRoutes(TestCase):

    def test_home_page(self):
        url = reverse('news:home')
        # Вызываем метод get для клиента (self.client)
        # и загружаем главную страницу.
        response = self.client.get(url)
        # Проверяем, что код ответа равен 200.
        self.assertEqual(response.status_code, HTTPStatus.OK)