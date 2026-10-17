# Shopwise

An original agentic-style shopping assistant demo. Its local workflow interprets
a shopper request, filters the catalog against a budget, ranks candidates with
TF-IDF similarity, and presents sample products. The catalog also supports
search, categories, and a demo cart.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

No API key, network catalog, or account is required. Products and prices are
illustrative. Recommendations are local text-similarity matches, not purchases.
The cart is local to the active Streamlit session; this app does not place
orders or process payments.

## Tests

```powershell
python -m unittest discover -s tests -v
```
