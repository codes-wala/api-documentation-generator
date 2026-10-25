from app.security import hash_password, verify_password, new_session_token, hash_token

def test_password_hash_does_not_equal_password_and_verifies():
    password = "a-very-long-test-password"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)

def test_tokens_are_random_and_hashed():
    first, second = new_session_token(), new_session_token()
    assert first != second
    assert hash_token(first) != first
    assert len(hash_token(first)) == 64
