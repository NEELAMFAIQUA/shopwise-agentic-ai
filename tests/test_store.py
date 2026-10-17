import unittest

from store import related_products, search_products, update_cart


class StoreTests(unittest.TestCase):
    def test_search_matches_product_and_category(self):
        self.assertEqual(search_products("mug")[0]["id"], "mug")
        self.assertEqual(search_products(category="Stationery")[0]["id"], "notebook")

    def test_cart_add_remove_and_zero_quantity(self):
        cart = update_cart({}, "mug", 1)
        self.assertEqual(cart, {"mug": 1})
        self.assertEqual(update_cart(cart, "mug", -1), {})

    def test_cart_rejects_invalid_delta(self):
        with self.assertRaises(ValueError):
            update_cart({}, "mug", 2)

    def test_recommendations_exclude_cart_and_share_tags(self):
        picks = related_products({"mug": 1})
        self.assertTrue(picks)
        self.assertNotIn("mug", [product["id"] for product in picks])
        self.assertIn("reusable", picks[0]["tags"])


if __name__ == "__main__":
    unittest.main()
