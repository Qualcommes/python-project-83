def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    
    assert 'Анализатор страниц' in html
    assert 'bootstrap.min.css' in html
    assert '<form' in html
    assert 'name="url"' in html
    assert 'Проверить' in html