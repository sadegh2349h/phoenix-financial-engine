from phoenix_core.public_social_provider import fetch_public_social_profile


def test_public_profile_parser_extracts_meta_and_public_counts(monkeypatch):
    class Response:
        text = '''<html><head>
        <meta property="og:title" content="Example Shop (@example)">
        <meta property="og:description" content="Example optical shop">
        </head><body>"edge_followed_by":{"count":1234},"edge_owner_to_timeline_media":{"count":56}</body></html>'''
        def raise_for_status(self):
            return None

    monkeypatch.setattr("phoenix_core.public_social_provider.requests.get", lambda *a, **k: Response())
    result = fetch_public_social_profile("https://www.instagram.com/example")
    assert result is not None
    assert result.username == "example"
    assert result.bio == "Example optical shop"
    assert result.followers == 1234
    assert result.posts == 56
