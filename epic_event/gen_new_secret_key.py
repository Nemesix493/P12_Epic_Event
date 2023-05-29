from django.core.management.utils import get_random_secret_key
print(f'"{get_random_secret_key()}"')