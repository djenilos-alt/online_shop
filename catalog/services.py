from django.core.cache import cache

from catalog.models import Product


CACHE_TTL = 60 * 15


def get_products_by_category(category_id):
    """
    Возвращает список продуктов указанной категории.
    Использует Redis для кеширования результата.
    """
    cache_key = f"category_{category_id}"

    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.filter(
                category_id=category_id
            ).select_related("category", "owner")
        )

        cache.set(cache_key, products, timeout=CACHE_TTL)

    return products
