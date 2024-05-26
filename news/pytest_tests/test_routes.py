from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('', ''),
        ('/news/', pytest.lazy_fixture('pk_for_url')),
        ('/auth/login', ''),
        ('/auth/logout', ''),
        ('/auth/signup', ''),
    )
)
def test_pages_availability(client, name, args):
    url = name + args + '/'
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('/edit_comment/', pytest.lazy_fixture('comment_pk_for_url')),
        ('/delete_comment/', pytest.lazy_fixture('comment_pk_for_url')),
    )
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, name, args, expected_status
):
    url = name + args + '/'
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('/edit_comment/', pytest.lazy_fixture('comment_pk_for_url')),
        ('/delete_comment/', pytest.lazy_fixture('comment_pk_for_url')),
    )
)
def test_redirect_for_anonymous_client(
    name, args, client
):
    login_url = '/auth/login/'
    url = name + args + '/'
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
