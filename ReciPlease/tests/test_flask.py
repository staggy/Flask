"""
https://flask.palletsprojects.com/en/2.0.x/testing/
Carl Gager's testing
"""
import pytest
from website import create_app
from pathlib import Path

app = create_app()

@pytest.fixture()
def app():
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_request_example(client):
    response = client.get("/posts")
    assert b"<h2>Hello, World!</h2>" in response.data


# def test_json_data(client):
#     response = client.post("/graphql", json={
#         "query": """
#             query User($id: String!) {
#                 user(id: $id) {
#                     name
#                     theme
#                     picture_url
#                 }
#             }
#         """,
#         variables={"id": 2},
#     })
#     assert response.json["data"]["user"]["name"] == "Flask"


def test_logout_redirect(client):
    response = client.get("/logout")
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # Check that the second request was to the index page.
    assert response.request.path == "/index"