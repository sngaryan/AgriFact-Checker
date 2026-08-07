import pytest
from services.domain_check import check_domains

def test_no_url():
    res = check_domains("This text has no links in it. Just standard text.")
    assert res["domain_status"] == "no_domain_found"
    assert res["detected_domain"] == ""

def test_verified_domain_exact():
    res = check_domains("Visit the official portal at https://pmkisan.gov.in for registration details.")
    assert res["domain_status"] == "verified"
    assert res["detected_domain"] == "pmkisan.gov.in"

def test_verified_domain_subdomain():
    res = check_domains("Please check http://sub.agriwelfare.gov.in/index.html to apply.")
    assert res["domain_status"] == "verified"
    assert res["detected_domain"] == "sub.agriwelfare.gov.in"

def test_lookalike_domain():
    res = check_domains("Urgent registration at http://pmkisan.gov.in.fake-portal.com/apply now!")
    assert res["domain_status"] == "not_in_list"
    assert res["detected_domain"] == "pmkisan.gov.in.fake-portal.com"

def test_lookalike_domain_hyphen():
    res = check_domains("Go to http://pmkisan.gov.in-fake.com for scheme subsidy.")
    assert res["domain_status"] == "not_in_list"
    assert res["detected_domain"] == "pmkisan.gov.in-fake.com"

def test_not_in_list_domain():
    res = check_domains("Click on https://example-blog.com/farming-tips to read more.")
    assert res["domain_status"] == "not_in_list"
    assert res["detected_domain"] == "example-blog.com"
