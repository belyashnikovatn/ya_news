from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(news, client, form_data):
    comments_count = Comment.objects.count()
    url = reverse('news:detail', args=(news.pk,))
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comments_count


@pytest.mark.django_db
def test_user_can_create_comment(news, author_client, form_data):
    comments_count = Comment.objects.count()
    url = reverse('news:detail', args=(news.pk,))
    response = author_client.post(url, data=form_data)
    expected_url = f'{url}#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == comments_count + 1


@pytest.mark.django_db
def test_user_cant_use_bad_words(news, author_client):
    comments_count = Comment.objects.count()
    url = reverse('news:detail', args=(news.pk,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=(WARNING))
    assert Comment.objects.count() == comments_count


@pytest.mark.django_db
def test_author_can_edit_note(author_client, form_data, news, comment):
    news_url = reverse('news:detail', args=(news.pk,))
    url = reverse('news:edit', args=(comment.pk,))
    response = author_client.post(url, form_data)
    assertRedirects(response, f'{news_url}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']


@pytest.mark.django_db
def test_author_can_delete_note(author_client, form_data, news, comment):
    comments_count = Comment.objects.count()
    news_url = reverse('news:detail', args=(news.pk,))
    url = reverse('news:delete', args=(comment.pk,))
    response = author_client.post(url, form_data)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == comments_count - 1


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(reader_client, form_data, comment):
    url = reverse('news:edit', args=(comment.pk,))
    response = reader_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.pk)
    assert comment.text == comment_from_db.text


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(reader_client, form_data, comment):
    comments_count = Comment.objects.count()
    url = reverse('news:delete', args=(comment.pk,))
    response = reader_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == comments_count
