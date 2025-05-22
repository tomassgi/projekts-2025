import pytest
from datetime import datetime, timedelta
from email_sending import is_valid_email, should_send

# --- Veiksmes scenāriji ---

def test_is_valid_email_success():
    assert is_valid_email("test@example.com") == True
    assert is_valid_email("user.name@domain.co") == True

def test_should_send_when_last_sent_none():
    # Ja iepriekš nav sūtīts, jāatgriež True
    assert should_send(None, 10) == True


# --- Lietošanas scenāriji ---

def test_should_send_with_delay_passed():
    last_sent = (datetime.now() - timedelta(seconds=30)).isoformat()
    assert should_send(last_sent, 10) == True

def test_should_send_with_delay_not_passed():
    last_sent = (datetime.now() - timedelta(seconds=5)).isoformat()
    assert should_send(last_sent, 10) == False

def test_is_valid_email_failure_cases():
    assert is_valid_email("plainaddress") == False
    assert is_valid_email("missing@domain") == False
    assert is_valid_email("missing_at_sign.com") == False

def test_is_valid_email_edge_cases():
    # Pārbauda e-pastus ar dažādiem simboliem un garumiem
    assert is_valid_email("a@b.c") == True
    assert is_valid_email("user+test@example.co.uk") == True


# --- Robež-scenāriji ---

def test_should_send_with_zero_delay():
    last_sent = datetime.now().isoformat()
    # Ja aizture ir 0 sekundes, vienmēr jāatgriež True
    assert should_send(last_sent, 0) == True

def test_should_send_with_future_last_sent():
    # Ja datums nākotnē, jāatgriež False
    future_time = (datetime.now() + timedelta(seconds=10)).isoformat()
    assert should_send(future_time, 5) == False