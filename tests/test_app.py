def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Анализатор страниц' in response.get_data(as_text=True)


def test_add_invalid_url(client):
    response = client.post('/urls', data={'url': 'invalid-url'})
    assert response.status_code == 422
    assert 'Некорректный URL' in response.get_data(as_text=True)


def test_add_url_and_redirect(client):
    response = client.post('/urls', data={'url': 'https://example.com/path'})
    assert response.status_code == 302
    assert response.headers['Location'].startswith('/urls/')


def test_create_check_with_mock(client, requests_mock):
    # 1. Добавляем URL
    response = client.post('/urls', data={'url': 'https://example.com'})
    
    # Извлекаем id из заголовка редиректа (например, '/urls/5' -> '5')
    url_id = response.headers['Location'].split('/')[-1]

    # 2. Мокируем внешний HTTP-запрос
    html_content = '<html><head><title>Test Title</title></head><body><h1>Test H1</h1></body></html>'
    requests_mock.get('https://example.com', text=html_content, status_code=200)

    # 3. Делаем проверку для ДЕЙСТВИТЕЛЬНО СОЗДАННОГО id
    response = client.post(f'/urls/{url_id}/checks', follow_redirects=True)
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'Страница успешно проверена' in html
    assert 'Test Title' in html
    assert 'Test H1' in html


def test_create_check_failed(client, requests_mock):
    response = client.post('/urls', data={'url': 'https://failing-site.com'})
    url_id = response.headers['Location'].split('/')[-1]

    # Мокируем ошибку 500
    requests_mock.get('https://failing-site.com', status_code=500)

    response = client.post(f'/urls/{url_id}/checks', follow_redirects=True)
    assert response.status_code == 200
    assert 'Произошла ошибка при проверке' in response.get_data(as_text=True)