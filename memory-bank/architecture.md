# Arsitektur Sistem: Rawat Tanam AI

## 1. Overview Arsitektur

### 1.1 Prinsip Desain
- **Hybrid Intelligence:** Kombinasi on-device dan cloud-based AI untuk optimal performance
- **API-First Architecture:** Platform terbuka dengan semua fitur accessible via REST API
- **Scalable & Resilient:** Arsitektur cloud-native yang dapat menangani pertumbuhan eksponensial
- **Privacy-First:** Minimalisasi data transfer dengan processing lokal dan GDPR compliance
- **Offline-Capable:** Fungsionalitas inti tetap berjalan tanpa koneksi internet
- **Modular Design:** Komponen loosely-coupled untuk maintainability dan integration flexibility

### 1.2 High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │    │   API Gateway   │    │  ML Pipeline    │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ On-device   │ │    │ │ Rate Limit  │ │    │ │ Training    │ │
│ │ ML Model    │ │    │ │ Auth        │ │    │ │ Pipeline    │ │
│ │ (TFLite)    │ │    │ │ Load Bal.   │ │    │ │             │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Local Cache │ │    │ │ API Router  │ │    │ │ Model       │ │
│ │ (SQLite)    │ │    │ │             │ │    │ │ Serving     │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ │ (TF Serving)│ │
└─────────────────┘    └─────────────────┘    │ └─────────────┘ │
         │                       │             └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                ┌─────────────────┴─────────────────┐
                │          Backend Services         │
                │                                   │
                │ ┌─────────────┐ ┌─────────────┐   │
                │ │ Species DB  │ │ User Data   │   │
                │ │ (PostgreSQL)│ │ Service     │   │
                │ └─────────────┘ └─────────────┘   │
                │                                   │
                │ ┌─────────────┐ ┌─────────────┐   │
                │ │ Image Store │ │ Analytics   │   │
                │ │ (Cloud)     │ │ Service     │   │
                │ └─────────────┘ └─────────────┘   │
                └───────────────────────────────────┘
```

## 2. Komponen Arsitektur

### 2.1 Mobile Application Layer

#### 2.1.1 Framework & Platform
- **Framework:** Flutter untuk cross-platform development
- **Target:** Android 8.0+ (API 26), iOS 12.0+
- **Architecture Pattern:** Clean Architecture dengan BLoC state management

#### 2.1.2 On-Device ML Model
- **Model:** EfficientNetV2-S optimized dengan Quantization-Aware Training
- **Format:** TensorFlow Lite (.tflite)
- **Size:** <50MB untuk model utama
- **Coverage:** 1000+ spesies paling umum di Indonesia
- **Performance Target:** <3 detik inference time

#### 2.1.3 Local Data Storage
- **Primary:** SQLite untuk species metadata dan cache
- **Secondary:** Shared Preferences untuk user settings
- **Images:** Local file system dengan LRU cache management
- **Sync Strategy:** Incremental sync dengan conflict resolution

#### 2.1.4 Camera & Image Processing
- **Camera API:** Native camera integration dengan custom UI
- **Image Preprocessing:** 
  - Auto-crop dengan edge detection
  - Brightness/contrast normalization
  - Resize to model input dimensions (224x224 atau 384x384)
- **Quality Checks:** Blur detection, lighting assessment

### 2.2 API Gateway Layer

#### 2.2.1 Technology Stack
- **Platform:** Google Cloud API Gateway atau AWS API Gateway
- **Protocol:** REST API dengan GraphQL untuk complex queries
- **Authentication:** JWT tokens dengan refresh mechanism
- **Rate Limiting:** Per-user dan per-endpoint limits

#### 2.2.2 Core Endpoints
```
POST /api/v1/identify
  - Input: Image file + metadata (location, timestamp)
  - Output: Species predictions dengan confidence scores

GET /api/v1/species/{id}
  - Output: Detailed species information

POST /api/v1/contribute
  - Input: User-submitted image + identification
  - Output: Contribution ID untuk tracking

GET /api/v1/search
  - Query parameters: name, family, habitat, location
  - Output: Paginated species list

POST /api/v1/user/collections
  - Input: Species ID + user notes
  - Output: Collection entry
```

### 2.3 Machine Learning Pipeline

#### 2.3.1 Training Infrastructure
- **Platform:** Google Cloud AI Platform atau AWS SageMaker
- **Compute:** GPU clusters (V100/A100) untuk training
- **Framework:** TensorFlow 2.x dengan Keras API
- **Orchestration:** Kubeflow Pipelines atau MLflow

#### 2.3.2 Model Architecture

**On-Device Model:**
- **Base:** EfficientNetV2-S (24M parameters)
- **Modifications:** 
  - Custom classification head untuk Indonesian species
  - Knowledge distillation dari larger teacher model
  - Quantization-Aware Training (INT8)
- **Input:** 224x224x3 RGB images
- **Output:** Probability distribution over 1000+ classes

**Cloud Model:**
- **Base:** EfficientNetV2-L atau Vision Transformer (ViT-L)
- **Ensemble:** Multiple models dengan voting mechanism
- **Input:** 384x384x3 atau 512x512x3 RGB images
- **Output:** Detailed predictions dengan uncertainty estimates

#### 2.3.3 Data Pipeline
- **Ingestion:** Automated data collection dari multiple sources
- **Preprocessing:** 
  - Image augmentation (rotation, flip, color jitter)
  - Background removal untuk herbarium specimens
  - Synthetic data generation untuk rare species
- **Validation:** Expert review workflow dengan active learning
- **Versioning:** DVC (Data Version Control) untuk dataset management

#### 2.3.4 Model Serving
- **Platform:** TensorFlow Serving dengan Kubernetes
- **Scaling:** Horizontal Pod Autoscaler berdasarkan request load
- **Caching:** Redis untuk frequent predictions
- **Monitoring:** Model performance metrics dan drift detection

### 2.4 Backend Services

#### 2.4.1 Species Database Service
- **Database:** PostgreSQL dengan PostGIS extension
- **Schema:**
  ```sql
  -- Species master table
  CREATE TABLE species (
    id UUID PRIMARY KEY,
    scientific_name VARCHAR(255) UNIQUE NOT NULL,
    common_names JSONB, -- Multiple languages
    family VARCHAR(100),
    genus VARCHAR(100),
    taxonomy JSONB, -- Full taxonomic hierarchy
    description TEXT,
    habitat TEXT,
    distribution GEOMETRY(MULTIPOLYGON, 4326),
    conservation_status VARCHAR(50),
    uses JSONB, -- Medicinal, ornamental, etc.
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
  );
  
  -- Reference images
  CREATE TABLE species_images (
    id UUID PRIMARY KEY,
    species_id UUID REFERENCES species(id),
    image_url VARCHAR(500),
    image_type VARCHAR(50), -- leaf, flower, fruit, bark
    source VARCHAR(100),
    license VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
  );
  ```

#### 2.4.2 User Data Service
- **Database:** PostgreSQL untuk relational data
- **Features:**
  - User profiles dan authentication
  - Personal collections dan notes
  - Contribution history dan gamification
  - Privacy settings dan consent management

#### 2.4.3 Image Storage Service
- **Primary:** Google Cloud Storage atau AWS S3
- **CDN:** CloudFlare untuk global distribution
- **Processing:** Cloud Functions untuk automatic image processing
- **Backup:** Cross-region replication

#### 2.4.4 Analytics Service
- **Platform:** Google Analytics 4 + Custom analytics
- **Metrics:**
  - User engagement dan retention
  - Model performance dalam production
  - Geographic usage patterns
  - Species identification trends

### 2.5 Data Flow Architecture

#### 2.5.1 Identification Flow
```
1. User captures image → Mobile App
2. Image preprocessing → On-device
3. Quick prediction → On-device Model
4. If confidence < threshold → Cloud API call
5. Enhanced prediction → Cloud Model
6. Result caching → Local Storage
7. Usage analytics → Analytics Service
```

#### 2.5.2 Contribution Flow
```
1. User submits image + ID → Mobile App
2. Upload to staging → Image Storage
3. Queue for review → Expert Review System
4. Validation process → Human-in-the-Loop
5. Approved data → Training Pipeline
6. Model retraining → ML Pipeline
7. Model deployment → Production
```

## 3. Deployment Architecture

### 3.1 Cloud Infrastructure
- **Platform:** Google Cloud Platform (primary) dengan AWS backup
- **Regions:** 
  - Primary: asia-southeast2 (Jakarta)
  - Secondary: asia-southeast1 (Singapore)
- **Networking:** VPC dengan private subnets untuk databases

### 3.2 Kubernetes Cluster
- **Orchestration:** Google Kubernetes Engine (GKE)
- **Node Pools:**
  - General workloads: n1-standard-4
  - ML inference: n1-highmem-8 dengan GPU
  - Database: n1-highmem-16 dengan SSD persistent disks

### 3.3 CI/CD Pipeline
- **Source Control:** Git dengan GitFlow branching strategy
- **CI/CD:** GitHub Actions atau GitLab CI
- **Deployment Strategy:** Blue-green deployment dengan canary releases
- **Testing:** Automated unit, integration, dan end-to-end tests

### 3.4 Monitoring & Observability
- **Metrics:** Prometheus + Grafana
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Tracing:** Jaeger untuk distributed tracing
- **Alerting:** PagerDuty integration untuk critical issues

## 4. API Platform Architecture

### 4.1 API Gateway Layer
- **Load Balancing:** Distribusi traffic across multiple instances
- **Rate Limiting:** Per-client dan per-endpoint rate limits
- **Authentication:** API key + OAuth 2.0 support
- **Request/Response Transformation:** Format standardization
- **Analytics:** Real-time API usage monitoring

### 4.2 API Tiers & Access Control
- **Free Tier:** 1,000 requests/month untuk developers
- **Professional Tier:** 10,000 requests/month dengan SLA
- **Enterprise Tier:** Unlimited dengan custom SLA
- **Partner Tier:** Special rates untuk strategic partners (e.g., Tanam Rawat)

### 4.3 External Integration Support
- **RESTful APIs:** Standard HTTP methods dan status codes
- **Webhook Support:** Real-time notifications untuk external systems
- **SDK Libraries:** Python, JavaScript, React Native, Java
- **Batch Processing:** Bulk identification untuk large datasets

### 4.4 Integration Examples
```yaml
Tanam Rawat Software:
  - Integration Type: Partner API
  - Endpoints: /identify, /species/{id}
  - Rate Limit: 500 req/min
  - SLA: <2s response time
  
Research Institutions:
  - Integration Type: Enterprise API
  - Endpoints: All endpoints + batch processing
  - Rate Limit: Unlimited
  - Custom Features: Model training, data export
  
Third-party Apps:
  - Integration Type: Professional API
  - Endpoints: Core identification features
  - Rate Limit: 100 req/min
  - Support: Email + documentation
```

## 5. Security Architecture

### 5.1 Data Protection
- **Encryption at Rest:** AES-256 untuk database dan storage
- **Encryption in Transit:** TLS 1.3 untuk semua communications
- **Key Management:** Google Cloud KMS atau AWS KMS
- **Data Classification:** Public, Internal, Confidential, Restricted

### 5.2 Authentication & Authorization
- **User Auth:** OAuth 2.0 dengan PKCE untuk mobile
- **API Auth:** JWT tokens dengan short expiration
- **Service-to-Service:** mTLS dengan certificate rotation
- **RBAC:** Role-based access control untuk admin functions
- **API Security:** API key rotation, IP whitelisting, DDoS protection

### 5.3 Privacy Compliance
- **GDPR/PDP Compliance:** Data minimization dan right to deletion
- **Consent Management:** Granular consent untuk different data uses
- **Data Retention:** Automated deletion berdasarkan retention policies
- **Audit Logging:** Comprehensive audit trail untuk data access
- **Cross-border Data Transfer:** Compliance dengan local regulations

## 6. Performance & Scalability

### 5.1 Performance Targets
- **Mobile App:** <3s cold start, <1s warm start
- **API Response:** <500ms untuk simple queries, <2s untuk ML inference
- **Database:** <100ms untuk read queries, <500ms untuk complex joins
- **Image Upload:** <10s untuk 5MB images

### 5.2 Scalability Strategy
- **Horizontal Scaling:** Stateless services dengan load balancers
- **Database Scaling:** Read replicas dan connection pooling
- **Caching Strategy:** Multi-layer caching (CDN, Redis, Application)
- **Auto-scaling:** Kubernetes HPA berdasarkan CPU/memory/custom metrics

### 5.3 Capacity Planning
- **Year 1:** 100K users, 1M identifications/month
- **Year 3:** 1M users, 10M identifications/month
- **Year 5:** 5M users, 50M identifications/month
- **Storage Growth:** 100GB/month untuk images dan data

## 7. Disaster Recovery & Business Continuity

### 6.1 Backup Strategy
- **Database:** Daily full backups + continuous WAL archiving
- **Images:** Cross-region replication dengan versioning
- **Code:** Git repositories dengan multiple remotes
- **Configuration:** Infrastructure as Code dengan Terraform

### 6.2 Recovery Procedures
- **RTO (Recovery Time Objective):** <4 hours untuk critical services
- **RPO (Recovery Point Objective):** <1 hour untuk data loss
- **Failover:** Automated failover untuk database dan services
- **Testing:** Quarterly disaster recovery drills

## 8. Future Considerations

### 7.1 Technology Evolution
- **Edge Computing:** Deploy models ke edge locations
- **5G Integration:** Leverage high-speed connectivity untuk real-time features
- **AR/VR:** Augmented reality untuk immersive plant identification
- **IoT Integration:** Smart sensors untuk environmental monitoring

### 7.2 Scalability Enhancements
- **Multi-region Deployment:** Global expansion dengan regional models
- **Microservices Migration:** Break monolith into smaller services
- **Event-driven Architecture:** Async processing dengan message queues
- **Serverless Computing:** Function-as-a-Service untuk variable workloads

Arsitektur ini dirancang untuk mendukung pertumbuhan jangka panjang sambil mempertahankan performance, security, dan user experience yang optimal. Setiap komponen dapat di-scale secara independen sesuai dengan kebutuhan bisnis dan teknis.