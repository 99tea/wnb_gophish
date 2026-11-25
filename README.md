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
