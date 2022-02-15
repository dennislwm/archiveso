import pytest

def test_app(client, header):
    objResponse = client.get("/", headers = header)
    assert objResponse.status_code == 200
    assert objResponse.data.find(b"App-version") >= 0
    assert objResponse.data.find(b"CLI-version: ArchiveBox")

def test_post_url_index_not_found(client, header):
    objResponse = client.post("/api/archiveso",
                              headers = header,
                              data={"url": "https://earthly.dev/blog/canary-deployment/"})
    assert objResponse.status_code == 503
    assert objResponse.data.find(b"Archivebox index not found") >= 0

def test_post_url_empty_form(client, header):
    objResponse = client.post("/api/archiveso", headers = header)
    assert objResponse.status_code == 400
    assert objResponse.data.find(b"Empty strUrl") >= 0