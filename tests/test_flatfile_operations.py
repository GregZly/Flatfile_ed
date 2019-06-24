from flatfileed import flatfile_operations

def test_index(client):
    response = client.get('/index')
    assert response.status_code == 200
    assert b'Modifiable CSV' in response.data
    