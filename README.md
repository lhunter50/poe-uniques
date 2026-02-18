# 🏹 PoE Uniques Explorer

A full-stack **Path of Exile Unique Item Explorer** built with **Django
(DRF) + PostgreSQL + Next.js**.

This project focuses on building a performant, league-aware unique item
browser with advanced filtering, tier-based sorting, and server-side
caching to minimize database load.

------------------------------------------------------------------------

## 🚀 Tech Stack

### Backend

-   Django
-   Django REST Framework
-   PostgreSQL
-   League-aware relational modeling
-   Annotated query sorting (Ancient tier, price, meta presence)
-   Custom pagination
-   Optional API response caching

### Frontend

-   Next.js (App Router)
-   Server Components
-   TailwindCSS
-   Query-parameter driven filtering & sorting
-   Server-side fetch caching (`revalidate`)

------------------------------------------------------------------------

## 📦 Features

### ✅ League-Aware Filtering

Only uniques present in the selected league are returned.

### ✅ Price Integration

Latest league stats per unique: - Chaos value - Divine value - Listing
count

### ✅ Ancient Orb Meta (Belts)

Integrated from poeladder: - Tier (0 = rarest) - Drop chance - Average
number of orbs - Minimum item level

### ✅ Intelligent Default Sorting

Backend default ordering: 1. Items with Ancient meta first\
2. Tier ascending (Tier 0 first)\
3. Chaos value descending\
4. Name (stable ordering)

### ✅ Belt-Focused Homepage

The homepage defaults to: - Belts - Ancient-tier-first sorting -
Chase-focused layout

### ✅ Pagination

Custom DRF pagination (default: 18 items per page).

### ✅ Server-Side Caching

To reduce database load: - Next.js fetch caching (`revalidate`) -
Optional DRF response caching - URL-based cache keys

Repeated refreshes do **not** repeatedly hit PostgreSQL.

------------------------------------------------------------------------

## 🧠 Architecture Overview

User\
↓\
Next.js (Server Component)\
↓\
Cached Fetch (`revalidate`)\
↓\
Django REST API\
↓\
PostgreSQL

------------------------------------------------------------------------

## 🔎 API Query Parameters

Supported filters:

-   `page`
-   `search`
-   `base_item__slot`
-   `ordering`
-   `league`

Example:

/api/uniques/?search=belt&ordering=-chaos_value&page=1

------------------------------------------------------------------------

## ⚙️ Local Development

### Backend Setup

cd backend\
python -m venv .venv\
source .venv/bin/activate (Windows:
.venv`\Scripts`{=tex}`\activate`{=tex})\
pip install -r requirements.txt\
python manage.py migrate\
python manage.py runserver

------------------------------------------------------------------------

### Frontend Setup

cd frontend\
npm install\
npm run dev

Create `.env.local`:

NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

------------------------------------------------------------------------

## 📊 Price & Meta Import

python manage.py update_prices --league Settlers

------------------------------------------------------------------------

## 🧩 Caching Strategy

Frontend:

fetch(url, { next: { revalidate: 3600 } })

Optional Backend:

@method_decorator(cache_page(60), name="dispatch")

------------------------------------------------------------------------

## 📈 Future Improvements

-   Category abstraction
-   Tier filtering
-   Price normalization
-   League switching UI
-   Redis caching layer
-   Automated scheduled price updates
-   API rate limiting
-   Production deployment

------------------------------------------------------------------------

## 📜 License

MIT
