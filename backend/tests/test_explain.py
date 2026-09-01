from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_explain_endpoint():
    r = client.get('/projects/1/explain-enhanced')
    assert r.status_code == 200
    j = r.json()
    assert 'chart_base64' in j
    assert j['chart_base64'].startswith('data:image/svg+xml;base64,')
    assert 'top_positive_contributors' in j
    assert 'top_negative_contributors' in j
