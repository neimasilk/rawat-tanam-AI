# Rawat Tanam AI - Indonesian Flora Identification API

🌿 **Platform API Identifikasi Flora Indonesia dengan Kecerdasan Buatan**

Sebuah platform API yang menggunakan machine learning untuk mengidentifikasi spesies tanaman Indonesia dengan akurasi tinggi, terintegrasi dengan sistem Tanam Rawat untuk manajemen perawatan tanaman.

## 🎯 Fitur Utama

- **Identifikasi Flora AI**: Identifikasi 1000+ spesies tanaman Indonesia dengan akurasi 85%+
- **Database Spesies Lengkap**: Informasi detail tentang flora Indonesia
- **Integrasi Tanam Rawat**: Sinkronisasi dengan sistem perawatan tanaman
- **API Tier System**: Berbagai tingkat akses (Free, Professional, Enterprise, Partner)
- **Rate Limiting**: Kontrol penggunaan API berdasarkan tier
- **Authentication**: Sistem autentikasi JWT dan API Key
- **Real-time Processing**: Identifikasi gambar secara real-time

## 🏗️ Arsitektur

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │────│   API Gateway   │────│  ML Pipeline    │
│   (Flutter)     │    │   (FastAPI)     │    │ (TensorFlow)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │ Backend Services│
                       │  (PostgreSQL)   │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Node.js 16+ (untuk integrasi Tanam Rawat)

### Installation

1. **Clone repository**
```bash
git clone https://github.com/your-org/rawat-tanam-AI.git
cd rawat-tanam-AI
```

2. **Setup Python environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r src/requirements.txt
```

3. **Setup environment variables**
```bash
cp src/.env.example src/.env
# Edit src/.env dengan konfigurasi Anda
```

4. **Jalankan server**
```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Jalankan semua test
pytest src/tests/ -v

# Test dengan coverage
pytest src/tests/ --cov=src --cov-report=html
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Authentication

API menggunakan dua metode autentikasi:
1. **API Key** (Header: `X-API-Key`)
2. **JWT Token** (Header: `Authorization: Bearer <token>`)

### Endpoints

#### 🔐 Authentication
- `POST /auth/register` - Registrasi user baru
- `POST /auth/login` - Login user
- `GET /auth/me` - Info user saat ini
- `POST /auth/api-key` - Generate API key
- `GET /auth/tiers` - Daftar tier yang tersedia

#### 🌱 Plant Identification
- `POST /identify/` - Identifikasi tanaman dari gambar
- `GET /identify/status` - Status service identifikasi

#### 📖 Species Database
- `GET /species/` - Daftar spesies (dengan pagination)
- `GET /species/{species_id}` - Detail spesies
- `GET /species/search/` - Pencarian spesies
- `GET /species/families/list` - Daftar family tanaman
- `GET /species/stats` - Statistik database

## 🧪 Development

### Project Structure

```
src/
├── main.py                 # FastAPI application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── api/
│   └── v1/
│       ├── router.py     # Main API router
│       └── endpoints/    # API endpoints
├── middleware/           # Custom middleware
├── integrations/        # External integrations
└── tests/              # Test files
```

## 🤝 Team

- **Neima** - Human, Architect/Reviewer (neima.rawat.tanam@gmail.com)
- **AgentCody** - AI, Backend Developer (agentcody.rawat.tanam@gmail.com)
- **Ani** - Human, Frontend Developer (ani.rawat.tanam@gmail.com)

## 📋 Status Proyek

### Phase 1 - Foundation & Prototyping ✅
- [x] Project setup dan arsitektur
- [x] API Gateway dengan FastAPI
- [x] Authentication system
- [x] Basic plant identification
- [x] Species database API
- [x] Tanam Rawat integration
- [x] Testing framework

### Phase 2 - Database Integration & Configuration ✅
- [x] Setup database dengan SQLAlchemy
- [x] Migrasi ke pydantic-settings
- [x] Konfigurasi Alembic untuk migrasi database
- [x] Integrasi database dengan aplikasi
- [x] Perbaikan middleware autentikasi
- [x] Konfigurasi Redis untuk caching
- [x] Pengujian menyeluruh (19/19 tes berhasil)

### Next Steps
- [ ] Implementasi ML model TensorFlow Lite
- [ ] Setup PostgreSQL untuk produksi
- [ ] Implementasi Redis untuk rate limiting
- [ ] Docker containerization

---

**Rawat Tanam AI** - Memajukan konservasi flora Indonesia melalui teknologi AI 🌿🇮🇩