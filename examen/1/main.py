from checker import (
    build_url, is_https, show_response, 
    check_site, scan_sites, check_headers, retry_check
)

print("=== Partea 1: build_url ===")
print('build_url("example.com", "login") ->', build_url("example.com", "login"))
print('build_url("example.com", "/login") ->', build_url("example.com", "/login"))

print("\n=== Partea 1: is_https ===")
print('is_https("https://example.com") ->', is_https("https://example.com"))
print('is_https("http://example.com") ->', is_https("http://example.com"))

print("\n=== Partea 2: show_response ===")
print("-> Site valid:")
show_response("https://example.com")
print("-> Site invalid (așteaptă eroare de conexiune):")
show_response("http://this-site-does-not-exist.invalid")

print("\n=== Partea 3: check_site ===")
print("-> Site valid:")
print(check_site("https://example.com"))
print("-> Site invalid:")
print(check_site("http://this-site-does-not-exist.invalid"))

print("\n=== Partea 4: scan_sites ===")
scan_sites()

print("\n=== Partea 5: check_headers ===")
print("-> Site cu anteturi:")
print(check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("-> Site invalid:")
print(check_headers("http://this-site-does-not-exist.invalid"))

print("\n=== Partea 6: retry_check ===")
print('retry_check("/status/200") ->', retry_check("https://httpbin.org/status/200"))
print('retry_check("/status/404") ->', retry_check("https://httpbin.org/status/404"))
print('retry_check("/status/500", attempts=3) ->', retry_check("https://httpbin.org/status/500"))
print('retry_check("/status/500", attempts=2) ->', retry_check("https://httpbin.org/status/500", attempts=2))
print('retry_check("invalid") ->', retry_check("http://this-site-does-not-exist.invalid"))

