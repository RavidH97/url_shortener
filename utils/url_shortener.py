import hashlib
from urllib.parse import urlparse
from django.db import IntegrityError
from url_shortener.models import UsedURL


def validate_url(url):
    """
    Validate the given URL.
    Returns True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  # Check if scheme and netloc are present
    except ValueError:
        return False


def generate_short_url(original_url):
    """
    Generate a short URL using MD5 hash.
    """
    index = 0
    md5_hash = hashlib.md5(original_url.encode()).hexdigest()
    while True:
        try:
            short_url = md5_hash[index:index+8]  # Use the next 8 characters of the MD5 hash as the short URL
            # Attempt to insert the short URL into the database
            used_url = UsedURL(short_url=short_url)
            used_url.save()
            return short_url
        except IntegrityError:
            index = index + 8


# Example usage:
if __name__ == "__main__":
    original_url = "https://www.mongodb.com/docs/mongodb-shell/connect/#std-label-mdb-shell-connect"

    # Validate the URL
    if validate_url(original_url):
        # Generate the short URL
        short_url = generate_short_url(original_url)
        print("Original URL:", original_url)
        print("Short URL:", short_url)
    else:
        print("Invalid URL")
