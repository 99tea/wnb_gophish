# 🎯 WNB Phisher (wnb_gophish)

> Containerized phishing simulation infrastructure built on [GoPhish](https://getgophish.com/).

![Docker](https://img.shields.io/badge/docker-compose-blue.svg)
![GoPhish](https://img.shields.io/badge/gophish-framework-orange.svg)
![Caddy](https://img.shields.io/badge/caddy-reverse%20proxy-00A9E0.svg)

## 📌 About

**WNB Phisher** is a Dockerized deployment stack that wraps **GoPhish** with supporting services to run authorized phishing simulation campaigns. It bundles a reverse proxy (Caddy), a Dropbox sync service, and a webhook listener, orchestrated via Docker Compose.

> ⚠️ **DISCLAIMER**: This project is intended **strictly for authorized security awareness training and penetration testing**. Using phishing tools against targets without explicit written permission is illegal and unethical. The author holds no responsibility for misuse.

## 🧱 Stack Overview

| Service | Description |
|---------|-------------|
| **gophish** | Core phishing simulation framework (campaigns, templates, landing pages) |
| **caddy** | Reverse proxy with automatic HTTPS/TLS |
| **dropbox_sync** | Syncs campaign artifacts/data with Dropbox |
| **webhook_listener** | Receives and processes webhook events (e.g., campaign opens/clicks) |

## 📂 Repository Structure

```
wnb_gophish/
├── caddy/                 # Caddy reverse proxy config
├── dropbox_sync/          # Dropbox sync service
├── gophish/               # GoPhish application
├── webhook_listener/      # Webhook event receiver
├── .env                   # Environment variables
├── docker-compose.yml     # Service orchestration
└── README.md
```

## 📦 Prerequisites

- Docker
- Docker Compose
- A domain (for HTTPS via Caddy)
- Dropbox API credentials (if using the sync service)

## ⚙️ Configuration

1. Copy and edit the environment file:

```bash
cp .env .env.local
# edit .env.local with your secrets and settings
```

2. Review `docker-compose.yml` to adjust service ports, volumes, and dependencies.

3. Configure Caddy (`caddy/`) with your domain for automatic TLS.

## 🚀 Deployment

Start the full stack:

```bash
docker-compose up -d
```

Check service status:

```bash
docker-compose ps
docker-compose logs -f
```

Access GoPhish through the Caddy-proxied endpoint (typically `https://<your-domain>`).

## 🔧 Services

### GoPhish
The core phishing framework. Manage campaigns, email templates, landing pages, and users through its admin interface.

### Caddy
Provides HTTPS termination and reverse proxying to GoPhish. Automatic TLS via Let's Encrypt.

### Dropbox Sync
Keeps campaign artifacts (e.g., exported data) synchronized with Dropbox.

### Webhook Listener
Listens for GoPhish webhook events (campaign opened, clicked, submitted data) and processes them.

## 📝 Notes

- Ensure you have **written authorization** before targeting any users or domains.
- Keep secrets (`.env`) out of version control.
- The original repository contains no LICENSE file — add one if you plan to distribute.
- Verify Caddy and Dropbox credentials before going live.

## 👤 Author

Developed by **99tea**
```

---

## Key Observations

- ✅ The repository is **infrastructure-focused** — Docker Compose + modular services — rather than a single script.
- ⚠️ The **original README is essentially empty** (just a title), so the proposed one adds substantial value.
- 🔍 **No LICENSE file** is present — recommend adding one (MIT/Apache) if distribution is intended.
- 🔐 The `.env` file is committed — verify it contains **no real secrets**; if it does, rotate them and use `.env.example` instead.
- 🧪 Folder contents (`gophish/`, `caddy/`, etc.) could not be inspected in detail from the extracted content; a deeper code review would require cloning the repo.
