# BlogAPI — High-Load Pragmatic Modular Monolith

A high-performance production-ready backend system designed to showcase advanced skills in Clean/Onion Architecture and high-load optimizations using Python. 

The primary goal of this repository is to demonstrate how to build scalable, strictly isolated domain-driven systems within a single process—avoiding the early-stage network overhead and tracing complexities of microservices.

---

## 🚀 Key Architectural Highlights & Skill Showcase

* **Modular Monolith with Onion Architecture:** The system is divided into fully isolated domains (`Identity` and `Content`) communicating purely in-memory via clean contracts/interfaces. 
* **Decoupled Layers (Strict Isolation):** * *Presentation (FastAPI Routers):* Handles HTTP concerns only, completely unaware of SQL. Dependency injection is streamlined via explicit factory methods.
    * *Domain Layer:* Contains pure business logic, remaining framework-agnostic and fully independent of FastAPI or database specifics.
    * *Infrastructure:* Manages external integrations (PostgreSQL, Redis, Notification workers).
* **Hybrid Real-Time Authentication System:** Optimized for high read loads. It utilizes stateless, cryptographically signed short-lived JWT Access Tokens to bypass database overhead. However, critical real-time bans are enforced via a quick, localized check against a Redis-backed `blacklist` cache.
* **Advanced Database Protections (PostgreSQL + SQLAlchemy):**
    * *Unit of Work Pattern:* Prevents middleware auto-committing. Transactions are strictly scoped and managed within the application layer.
    * *No N+1 Queries:* Database relations are fetched explicitly using eager loading (`selectinload` / `joinedload`) directly in repository contracts.
    * *Keyset (Cursor-Based) Pagination:* High-performance heavy feed scanning utilizing `WHERE id < last_seen_id` instead of sluggish database `OFFSET`.
    * *Data Denormalization:* Read counters are tracked inside core tables and updated transactionally to eliminate expensive `COUNT(*)` runtime execution.
* **Aggressive Caching & Invalidation:** Heavy read data (e.g., feed feeds) is mirrored in Redis with immediate eager cache invalidation routines triggered upon data modification.

---

## 🛠️ Technology Stack

* **Framework:** FastAPI (Asynchronous execution)
* **Storage:** PostgreSQL + SQLAlchemy 2.0 (Async ORM)
* **Caching & Sessions:** Redis (Async drivers)
* **Environment:** Docker / Docker Compose
* **Security:** Cryptographic JWT signing (RSA-2048) & Bcrypt password hashing

---

## 📦 Project Dependencies

Before cloning the repository, ensure you have the following installed on your host system:
* `Docker` (Engine version 20.10+)
* `Docker Compose` (V2 syntax supported)
* `OpenSSL` (Used locally by the startup script for key management)

---

## ⚡ Quick Start (Foolproof Local Deployment)

The project includes an intelligent, idempotent initialization script that automates environment templating, key generation, and service orchestrations.

### 1. Clone the repository
```bash
    git clone [https://github.com/sultankurb/BlogAPI.git](https://github.com/sultankurb/BlogAPI.git)
    cd BlogAPI
    chmod +x start.sh
    ./start.sh
```

What the script does automatically on its first run:

    Detects missing configurations and instantiates local defaults (.env, docker/postgres.env, docker/redis.acl) from .example templates.

    Creates the certificates/ directory and safely generates fresh RSA-2048 private and public keys for secure JWT signing.

    Automatically orchestrates, builds, and starts all Docker infrastructure containers in detached mode.


```
  📂 Architecture Blueprint
    src/
    ├── config/                # Global settings, exception handlers, and JWT configuration
    ├── domain/                # Pure business logic (Framework-agnostic)
    │   ├── identity/          # User records, security rules, tokens
    │   └── content/           # Posts, commentaries, feed logic
    │
    ├── infrastructure/        # Shared infrastructure
    │   ├── database/          # SQLAlchemy engine and Unit of Work setup
    │   ├── redis/             # Redis pooling config
    │   └── notifications/     # Notification services (e.g., email, SMS)
    │
    └── presentation/          # API Delivery Layer
        ├── api/
        │   ├── identity/
        │   │   ├── router.py      # HTTP routes for identity actions
        │   │   └── dependencies.py     # Explicit injection factories for Identity domain
        │   └── content/
        │       ├── router.py      # HTTP routes for blog actions
        │       └── dependencies.py     # Explicit injection factories for Content domain
        └── middleware/            # Custom FastAPI middleware
```