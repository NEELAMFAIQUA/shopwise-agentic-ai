"""An original shopping discovery and cart demo."""

import streamlit as st

from store import PRODUCTS, related_products, search_products, update_cart

st.set_page_config(page_title="Shopwise", page_icon="🛍️")
st.title("Shopwise")
st.caption("Explore a sample catalog, compare products, and build a demo cart.")
st.info("Sample catalog only. This demo does not process orders or payments.")

if "cart" not in st.session_state:
    st.session_state.cart = {}

query = st.text_input("Search products")
categories = sorted({product["category"] for product in PRODUCTS})
category = st.selectbox("Category", ["All", *categories])
matches = search_products(query, category)

if matches:
    cols = st.columns(2)
    for index, product in enumerate(matches):
        with cols[index % 2]:
            st.subheader(product["name"])
            st.caption(f"{product['category']} · ${product['price']:.2f}")
            st.write("Tags: " + ", ".join(product["tags"]))
            if st.button("Add to cart", key=f"add-{product['id']}"):
                st.session_state.cart = update_cart(
                    st.session_state.cart, product["id"], 1
                )
                st.rerun()
else:
    st.warning("No products match that search.")

st.divider()
st.header("Your demo cart")
cart_products = [
    (product, st.session_state.cart[product["id"]])
    for product in PRODUCTS if st.session_state.cart.get(product["id"], 0) > 0
]
if cart_products:
    for product, quantity in cart_products:
        left, right = st.columns([4, 1])
        left.write(f"{product['name']} × {quantity} — ${product['price'] * quantity:.2f}")
        if right.button("Remove", key=f"remove-{product['id']}"):
            st.session_state.cart = update_cart(
                st.session_state.cart, product["id"], -1
            )
            st.rerun()
    total = sum(product["price"] * quantity for product, quantity in cart_products)
    st.metric("Demo subtotal", f"${total:.2f}")
    st.caption("Taxes and shipping are not included; checkout is intentionally disabled.")

if cart_products:
    recommendations = related_products(st.session_state.cart)
    if recommendations:
        st.subheader("Related picks")
        st.write(", ".join(f"{p['name']} (${p['price']:.2f})" for p in recommendations))
