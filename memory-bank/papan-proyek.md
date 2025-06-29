# Papan Proyek: Rawat Tanam AI

### STATUS [Update: 2024-12-19]
- **Tahap:** Inisialisasi Proyek (Phase 1 - Foundation & Prototyping)
- **Progress:** Spesifikasi produk dan arsitektur sistem telah selesai dibuat
- **Next:** Setup infrastruktur dasar dan prototype development

### REFERENSI ARSIP
- Belum ada baby-step sebelumnya (ini adalah baby-step pertama)

### BABY-STEP BERJALAN: API Platform Development & Tanam Rawat Integration

**Tujuan:** Membangun API platform yang dapat diintegrasikan dengan Tanam Rawat Software dan aplikasi eksternal lainnya

**Context:** Berdasarkan analisis software Tanam Rawat yang sudah ada, kita perlu membangun API platform yang dapat menyediakan layanan identifikasi flora untuk integrasi eksternal.

**Tugas:**

1. **T1: API Gateway & Authentication Setup** | **File:** `src/api-gateway/`, `src/auth/` | **Tes:** API Gateway dapat handle authentication dan rate limiting | **Assignee:** AgentCody
   - Setup API Gateway dengan FastAPI
   - Implementasi API key authentication
   - Rate limiting per tier (Free, Professional, Enterprise, Partner)
   - JWT token validation
   - Request/response logging

2. **T2: Core Identification API Development** | **File:** `src/backend/api/v1/identify.py` | **Tes:** Endpoint `/v1/identify` dapat menerima gambar dan mengembalikan hasil mock | **Assignee:** AgentCody
   - POST /v1/identify endpoint dengan file upload
   - Image validation dan preprocessing
   - Mock ML model integration
   - Response format sesuai API specification
   - Error handling dan status codes

3. **T3: Species Database API** | **File:** `src/backend/api/v1/species.py`, `src/backend/models/species.py` | **Tes:** CRUD operations untuk species data berfungsi | **Assignee:** AgentCody
   - Database schema untuk species information
   - GET /v1/species/{id} endpoint
   - GET /v1/species/search dengan filtering
   - Species data seeding (minimal 100 species)
   - Pagination dan sorting

4. **T4: Tanam Rawat Integration Client** | **File:** `src/integrations/tanam_rawat_client.py` | **Tes:** Client dapat berkomunikasi dengan Tanam Rawat backend | **Assignee:** AgentCody
   - HTTP client untuk komunikasi dengan Tanam Rawat
   - Response transformation untuk compatibility
   - Error handling dan retry mechanism
   - Integration testing dengan mock Tanam Rawat API

5. **T5: API Documentation & SDK Prototype** | **File:** `docs/api/`, `src/sdk/python/` | **Tes:** API documentation accessible dan Python SDK dapat melakukan basic calls | **Assignee:** Ani
   - OpenAPI/Swagger documentation
   - Interactive API explorer
   - Python SDK prototype
   - Code examples dan tutorials
   - Postman collection

6. **T6: Monitoring & Analytics Setup** | **File:** `src/monitoring/`, `src/analytics/` | **Tes:** API metrics dapat ditrack dan dashboard accessible | **Assignee:** Ani
   - API usage analytics
   - Performance monitoring
   - Error tracking dan alerting
   - Basic dashboard untuk API metrics
   - Health check endpoints

### SARAN & RISIKO

**Saran Teknis:**
1. **Technology Stack Recommendation:**
   - Backend: FastAPI dengan Python untuk API platform development
   - Database: PostgreSQL dengan Docker untuk development
   - API Gateway: FastAPI dengan rate limiting dan authentication
   - ML: TensorFlow Lite untuk on-device inference

2. **Development Workflow:**
   - Gunakan Docker Compose untuk setup environment yang konsisten
   - Implementasi basic CI/CD dengan GitHub Actions
   - Setup linting dan formatting tools (Black, isort, flake8)

3. **Data Strategy:**
   - Mulai dengan dataset kecil (Indonesian Herb Leaf Dataset 3500) untuk prototype
   - Implementasi basic image preprocessing pipeline
   - Setup data validation dan quality checks

### TEKNOLOGI YANG DIREKOMENDASIKAN

**API Platform:**
- **API Gateway:** FastAPI dengan Uvicorn
- **Authentication:** JWT + API Key authentication
- **Rate Limiting:** Redis-based rate limiting
- **Documentation:** OpenAPI/Swagger dengan ReDoc
- **Monitoring:** Prometheus + Grafana

**Backend Services:**
- **Runtime:** Python 3.11+
- **Framework:** FastAPI untuk high-performance APIs
- **Database:** PostgreSQL 15+ dengan PostGIS extension
- **ORM:** SQLAlchemy dengan Alembic migrations
- **Caching:** Redis untuk session dan rate limiting

**ML/AI:**
- **Framework:** TensorFlow Lite untuk on-device
- **Cloud ML:** TensorFlow Serving atau PyTorch Serve
- **Image Processing:** OpenCV atau PIL
- **Model Format:** TFLite, ONNX
- **Model Serving:** TensorFlow Serving dengan gRPC

**Integration & SDKs:**
- **HTTP Client:** httpx untuk async requests
- **SDK Languages:** Python, JavaScript/Node.js, React Native
- **Webhook:** FastAPI background tasks
- **Batch Processing:** Celery dengan Redis broker

**Infrastructure:**
- **Containerization:** Docker + Docker Compose
- **Cloud:** Google Cloud Platform (API Gateway, Cloud Run)
- **CI/CD:** GitHub Actions dengan automated testing
- **Monitoring:** Prometheus + Grafana + Sentry

**Risiko yang Teridentifikasi:**
1. **Kompleksitas ML Model:** 
   - **Risiko:** Model training membutuhkan computational resources yang besar
   - **Mitigasi:** Mulai dengan pre-trained model dan fine-tuning, gunakan cloud resources untuk training

2. **Data Quality & Availability:**
   - **Risiko:** Dataset Indonesia flora masih terbatas dan tersebar
   - **Mitigasi:** Fokus pada spesies umum dulu, setup partnership dengan institusi penelitian

3. **Mobile Performance:**
   - **Risiko:** On-device ML model dapat mempengaruhi performance aplikasi
   - **Mitigasi:** Implementasi model optimization (quantization), fallback ke cloud inference

4. **Scalability Concerns:**
   - **Risiko:** Architecture mungkin tidak scale untuk 100K+ users
   - **Mitigasi:** Design dengan microservices pattern, implementasi caching strategy

**Dependencies & Prerequisites:**
- Docker & Docker Compose installed
- Flutter SDK (latest stable version)
- Node.js 18+ dan npm/yarn
- PostgreSQL 14+
- Git dengan proper SSH keys setup

**Estimasi Waktu:**
- T1: 2-3 hari
- T2: 2-3 hari  
- T3: 2-3 hari
- T4: 2-3 hari
- T5: 1-2 hari
- T6: 1-2 hari
- **Total:** 10-14 hari kerja

**Dependencies:**
- T2 depends on T1 (API Gateway harus ready)
- T3 depends on T1 (authentication system harus ada)
- T4 depends on T2 dan T3 (core APIs harus functional)
- T5 depends on T2 dan T3 (APIs harus documented)
- T6 dapat dikerjakan parallel dengan tasks lain

**Success Criteria untuk Baby-Step:**
✅ API Gateway dapat handle authentication dan rate limiting
✅ Core identification endpoint dapat menerima gambar dan mengembalikan mock results
✅ Species database API dapat melakukan CRUD operations
✅ Integration client untuk Tanam Rawat Software berfungsi
✅ API documentation accessible dan interactive
✅ Python SDK prototype dapat melakukan basic API calls
✅ Monitoring dashboard menampilkan API metrics
✅ End-to-end testing dari external client ke API berhasil

**Target Deliverable:**
- Functional API platform yang dapat diintegrasikan dengan Tanam Rawat Software
- Comprehensive API documentation dengan examples
- Working SDK prototype untuk Python
- Monitoring dan analytics dashboard
- Clear integration guide untuk external developers

---

### 🔗 REFERENSI PANDUAN
- **📊 Lihat ringkasan proyek**: `memory-bank/summary-report.md` atau `./vibe-guide/init_vibe.sh --dashboard`
- **Jika mengalami bug kompleks**: Lihat [Panduan Debugging & Git Recovery](./DEBUGGING_GIT.md)
- **Untuk review kode**: Konsultasi dengan [Dokumenter](./roles/dokumenter.md)
- **Untuk testing**: Koordinasi dengan [Tester](./roles/tester.md)
- **Untuk arsitektur**: Diskusi dengan [Arsitek](./roles/arsitek.md)
