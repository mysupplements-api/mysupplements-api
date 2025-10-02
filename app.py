from typing import List, Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware

class Product(BaseModel):
    id: str
    title: str
    price: float
    currency: str
    product_url: HttpUrl
    image_url: HttpUrl
    brand: str = "MySupplements"
    availability: str = "in_stock"
    mpn: Optional[str] = None
    gtin: Optional[str] = None
    country: str = "CH"

DB: List[Product] = [
    Product(
        id="MS-SHIL-50",
        title="Himalaya Shilajit Harz – 50g",
        price=29.90,
        currency="CHF",
        
product_url="https://mysupplements.ch/collections/himalaya-shilajit/products/himalaya-shilajit-harz",
        
image_url="https://cdn.shopify.com/s/files/1/0915/9891/3865/files/Golden.png?v=1752315616",
        mpn="MS-SHIL-50",
        country="CH",
    ),
    Product(
        id="MS-NMN-RES-60",
        title="NMN + Resveratrol Kapseln – 60 Stück",
        price=25.90,
        currency="CHF",
        
product_url="https://mysupplements.ch/collections/longevity/products/mysupplements-nmn-resveratrol-zellenergie-langlebigkeit",
        
image_url="https://cdn.shopify.com/s/files/1/0915/9891/3865/files/17C0ED8D-FA81-414B-9A6A-22A54ED7E802.jpg?v=1752592972",
        mpn="MS-NMN-RES-60",
        country="CH",
    ),
    Product(
        id="MS-SPERM-90",
        title="Spermidin Kapseln – 60 Stück",
        price=27.90,
        currency="CHF",
        
product_url="https://mysupplements.ch/collections/longevity/products/spermidin",
        image_url="https://cdn.shopify.com/s/files/1/0915/9891/3865/files/7AA08625-D373-44AC-B2F0-E95F46CBD0BD.jpg?v=1752315358",
        mpn="MS-SPERM-90",
        country="CH",
    ),
]

app = FastAPI(title="MySupplements Shopping API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search", response_model=List[Product])
def search(
    q: Optional[str] = Query(None, description="Suchbegriff"),
    country: Optional[str] = Query(None, description="CH, DE, AT"),
    limit: int = Query(8, ge=1, le=24),
):
    def matches(p: Product) -> bool:
        if country and p.country.upper() != country.upper():
            return False
        if not q:
            return True
        needle = q.lower()
        hay = f"{p.title} {p.brand} {p.mpn or ''}".lower()
        return all(token in hay for token in needle.split())

    results = [p for p in DB if matches(p)]
    return results[:limit]

@app.get("/product/{pid}", response_model=Product)
def get_product(pid: str):
    for p in DB:
        if p.id == pid:
            return p
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Product not found")

