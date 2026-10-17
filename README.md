# Shopwise

An original shopping discovery demo with a sample catalog, product search,
transparent tag-based recommendations, and a stateful demo cart.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

No API key, network catalog, or account is required. Products and prices are
illustrative. The cart is local to the active Streamlit session; this app does
not place orders or process payments.

## Tests

```powershell
python -m unittest discover -s tests -v
```
