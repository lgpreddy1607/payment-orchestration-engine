import pytest

from domain.value_objects import IdempotencyKey
from domain.exceptions import InvariantViolation


def test_valid_idempotency_key():
    key = IdempotencyKey("abc123")
    assert key.value == "abc123"


def test_whitespace_is_stripped():
    key = IdempotencyKey("  abc123  ")
    assert key.value == "abc123"


def test_empty_string_fails():
    with pytest.raises(InvariantViolation):
        IdempotencyKey("")


def test_whitespace_only_fails():
    with pytest.raises(InvariantViolation):
        IdempotencyKey("   ")


def test_non_string_fails():
    with pytest.raises(InvariantViolation):
        IdempotencyKey(123)  # type: ignore


def test_too_long_key_fails():
    long_key = "a" * 256
    with pytest.raises(InvariantViolation):
        IdempotencyKey(long_key)


def test_equality():
    k1 = IdempotencyKey("abc123")
    k2 = IdempotencyKey("abc123")
    k3 = IdempotencyKey("different")

    assert k1 == k2
    assert k1 != k3