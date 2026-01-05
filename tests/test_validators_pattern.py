"""
Test suite for inputkit.validators.patterns module.

Covers all pattern classes: UsernamePattern, FullNamePattern, EmailPattern, URLPattern, FilePathPattern, CommandPattern, MultiLineTextPattern,
IntegerPattern, FloatPattern, PercentagePattern, YearPattern, AgePattern, BooleanPattern, PinPattern, ApiKeyPattern, TokenPattern,
MobileNumberPattern.
"""
import pytest
from inputkit.validators.patterns import (
    UsernamePattern, FullNamePattern, EmailPattern, URLPattern, FilePathPattern, CommandPattern,
    MultiLineTextPattern, IntegerPattern, FloatPattern, PercentagePattern, YearPattern, AgePattern,
    BooleanPattern, PinPattern, ApiKeyPattern, TokenPattern, MobileNumberPattern
)

class TestUsernamePattern:
    def test_strict_valid(self):
        assert UsernamePattern.is_valid("user_name-123")
    def test_strict_invalid(self):
        assert not UsernamePattern.is_valid("user@name")
    def test_relaxed_valid(self):
        assert UsernamePattern.is_valid("نام_کاربری123", strict=False)

class TestFullNamePattern:
    def test_basic(self):
        assert FullNamePattern.is_valid("Ali Reza")
        assert FullNamePattern.is_valid("René Descartes")
        assert FullNamePattern.is_valid("Mary-Jane O'Neil")
    def test_invalid(self):
        assert not FullNamePattern.is_valid("A ")
        assert not FullNamePattern.is_valid("123$@")

class TestEmailPattern:
    @pytest.mark.parametrize("email,expect", [
        ("test@example.com", True),
        ("bad_email@", False), ("user@sub.domain.co.uk", True),
        ("user@domain", False)
    ])
    def test_various(self, email, expect):
        assert EmailPattern.is_valid(email) == expect

class TestURLPattern:
    @pytest.mark.parametrize("url,expect", [
        ("https://example.com", True),
        ("ftp://host.name/file.txt", True),
        ("file:///c:/windows/path", True),
        ("not//valid", False)
    ])
    def test_urls(self, url, expect):
        assert URLPattern.is_valid(url) == expect

class TestFilePathPattern:
    def test_unix(self):
        assert FilePathPattern.is_valid("/usr/local/bin/file.sh")
    def test_windows(self):
        assert FilePathPattern.is_valid(r"C:\\Users\\user\\Desktop\\file.txt")
    def test_invalid(self):
        assert not FilePathPattern.is_valid("$home/bin/file.txt")

class TestCommandPattern:
    def test_basic(self):
        assert CommandPattern.is_valid("ls -la /tmp")
        assert not CommandPattern.is_valid("echo Hello | grep x; rm -rf /") # semi-invalid

class TestMultiLineTextPattern:
    def test_multiline(self):
        assert MultiLineTextPattern.is_valid("first\nsecond line")
        assert not MultiLineTextPattern.is_valid("one line only")

class TestIntegerPattern:
    @pytest.mark.parametrize("text,expect", [
        ("123", True), ("-42", True), ("+0", True), ("1.25", False)
    ])
    def test_int(self, text, expect):
        assert IntegerPattern.is_valid(text) == expect
    def test_positive(self):
        assert IntegerPattern.is_positive("123")
        assert not IntegerPattern.is_positive("-1")
    def test_negative(self):
        assert IntegerPattern.is_negative("-33")
        assert not IntegerPattern.is_negative("77")

class TestFloatPattern:
    @pytest.mark.parametrize("text,expect", [
        ("3.14", True), ("-0.001", True), ("2.", True), ("5", False)
    ])
    def test_float(self, text, expect):
        assert FloatPattern.is_valid(text) == expect
    def test_positive(self):
        assert FloatPattern.is_positive("1.23")
        assert not FloatPattern.is_positive("-1.23")
    def test_negative(self):
        assert FloatPattern.is_negative("-4.5")
        assert not FloatPattern.is_negative("9.5")

class TestPercentagePattern:
    @pytest.mark.parametrize("text,expect", [
        ("100", True), ("100%", True), ("45.5%", True), ("123", False)
    ])
    def test_pct(self, text, expect):
        assert PercentagePattern.is_valid(text) == expect

class TestYearPattern:
    def test_valid_year(self):
        assert YearPattern.is_valid("2000")
        assert YearPattern.is_valid("1999")
        assert not YearPattern.is_valid("1899")
        assert not YearPattern.is_valid("2100")

class TestAgePattern:
    @pytest.mark.parametrize("age,expect", [
        ("0", True), ("21", True), ("99", True), ("150", True), ("151", False), ("-1", False)
    ])
    def test_age(self, age, expect):
        assert AgePattern.is_valid(age) == expect

class TestBooleanPattern:
    @pytest.mark.parametrize("text,expect", [
        ("yes", True), ("Y", True), ("n", True), ("TrUe", True), ("false", True), ("off", True), ("sure", True), ("maybe", False)
    ])
    def test_bool_variants(self, text, expect):
        assert BooleanPattern.is_valid(text) == expect

class TestPinPattern:
    def test_pins(self):
        assert PinPattern.is_valid("1234")
        assert PinPattern.is_valid("123456789012")
        assert not PinPattern.is_valid("123")
        assert not PinPattern.is_valid("notapin")

class TestApiKeyPattern:
    def test_api_keys(self):
        assert ApiKeyPattern.is_valid("a" * 32)
        assert ApiKeyPattern.is_valid("api_KEY-1234567890abcdefABCDEF_09876")
        assert not ApiKeyPattern.is_valid("short")
        assert not ApiKeyPattern.is_valid("!@#$%^&*")

class TestTokenPattern:
    def test_tokens(self):
        assert TokenPattern.is_valid("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9")
        assert TokenPattern.is_valid("deadbeef1234==")
        assert not TokenPattern.is_valid(" ")
        assert not TokenPattern.is_valid("token!")

class TestMobileNumberPattern:
    def test_e164(self):
        assert MobileNumberPattern.is_valid("+989121234567")
        assert not MobileNumberPattern.is_valid("989121234567")
    def test_iran(self):
        assert MobileNumberPattern.is_valid("09121234567", country="IR")
        assert MobileNumberPattern.is_valid("+989121234567", country="IR")
        assert not MobileNumberPattern.is_valid("08121234567", country="IR")
    def test_us(self):
        assert MobileNumberPattern.is_valid("+12025550123", country="US")
        assert not MobileNumberPattern.is_valid("2025550123", country="IR")
    def test_uk(self):
        assert MobileNumberPattern.is_valid("+447911123456", country="UK")
        assert not MobileNumberPattern.is_valid("071234", country="UK")
