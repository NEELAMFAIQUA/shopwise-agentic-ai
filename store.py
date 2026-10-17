"""Sample catalog and transparent product discovery helpers."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

PRODUCTS = [
    {"id": "mug", "name": "Ceramic travel mug", "category": "Home", "price": 18.50, "tags": ["reusable", "coffee"]},
    {"id": "lamp", "name": "Adjustable desk lamp", "category": "Home", "price": 42.00, "tags": ["lighting", "study"]},
    {"id": "bottle", "name": "Insulated water bottle", "category": "Outdoors", "price": 24.00, "tags": ["reusable", "travel"]},
    {"id": "pack", "name": "Everyday daypack", "category": "Outdoors", "price": 56.00, "tags": ["travel", "storage"]},
    {"id": "notebook", "name": "Recycled-paper notebook", "category": "Stationery", "price": 8.00, "tags": ["study", "reusable"]},
    {"id": "headphones", "name": "Wired studio headphones", "category": "Electronics", "price": 39.00, "tags": ["audio", "study"]},
]


def search_products(query="", category="All", products=None):
    query = query.strip().lower()
    catalog = PRODUCTS if products is None else products
    return [
        product for product in catalog
        if (category == "All" or product["category"] == category)
        and (not query or query in " ".join(
            [product["name"], product["category"], *product["tags"]]
        ).lower())
    ]


def agentic_recommendation_flow(query, budget, products=None, limit=5):
    """Run independent intent, catalog, budget, and ranking stages locally."""
    if budget <= 0:
        raise ValueError("budget must be positive")
    catalog = PRODUCTS if products is None else products
    query_terms = query.strip()
    eligible = [product for product in catalog if product["price"] <= budget]
    if not eligible or not query_terms:
        return {"intent": query_terms, "budget_matches": eligible, "ranked": []}

    descriptions = [
        f"{product['name']} {product['category']} {' '.join(product['tags'])}"
        for product in eligible
    ]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([query_terms, *descriptions])
    scores = cosine_similarity(matrix[0:1], matrix[1:]).ravel()
    ranked = sorted(
        zip(scores, eligible),
        key=lambda pair: (-float(pair[0]), pair[1]["price"], pair[1]["id"]),
    )
    return {
        "intent": query_terms,
        "budget_matches": eligible,
        "ranked": [
            {**product, "match_score": float(score)}
            for score, product in ranked[:limit]
            if score > 0
        ],
    }


def update_cart(cart, product_id, delta):
    """Return a new cart with a non-negative quantity."""
    if delta not in (-1, 1):
        raise ValueError("delta must be -1 or 1")
    updated = dict(cart)
    quantity = updated.get(product_id, 0) + delta
    if quantity > 0:
        updated[product_id] = quantity
    else:
        updated.pop(product_id, None)
    return updated


def related_products(cart, products=None, limit=3):
    catalog = PRODUCTS if products is None else products
    selected = {product["id"] for product in catalog if cart.get(product["id"], 0)}
    tags = {
        tag for product in catalog if product["id"] in selected
        for tag in product["tags"]
    }
    ranked = [
        (len(tags.intersection(product["tags"])), index, product)
        for index, product in enumerate(catalog)
        if product["id"] not in selected and tags.intersection(product["tags"])
    ]
    ranked.sort(key=lambda row: (-row[0], row[1]))
    return [row[2] for row in ranked[:limit]]
