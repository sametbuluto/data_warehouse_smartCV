# SmartCV — AI Candidate Matching Platform

SmartCV, üniversite seviyesi sunum ve demo odaklı geliştirilen bir yapay zeka destekli aday eşleştirme platformudur.

Bu proje, yüklenen CV’leri analiz eder, aday bilgilerini çıkarır, iş ilanlarını yapılandırılmış biçimde saklar, adayları iş ilanlarıyla eşleştirir, sıralar ve neden o sonucu verdiğini açıklanabilir bir şekilde gösterir.

Sistem production-scale bir hiring platformu olmayı hedeflemez. Hedefi şunlardır:

- akademik olarak anlaşılır bir NLP/ML pipeline sunmak
- lokal ortamda stabil çalışan bir demo üretmek
- profesyonel görünümlü bir SaaS dashboard deneyimi sağlamak
- canlı sunumda etkileyici bir UI/UX ile güven vermek
- aday eşleştirme mantığını açıklanabilir hale getirmek

---

## 1. Projenin Amacı

SmartCV’nin temel amacı, işe alım sürecindeki şu adımları tek bir sistemde birleştirmektir:

1. CV yükleme
2. CV içinden aday bilgisini çıkarma
3. Yetenekleri, deneyimi ve eğitimi normalize etme
4. İş ilanı oluşturma
5. Aday ile iş ilanı arasındaki uyumu hesaplama
6. Adayları sıralama
7. Eşleşme skorunu görselleştirme
8. Eşleşme nedenlerini açıklama

Bu yönüyle sistem, klasik CRUD projesinden daha fazlasını yapar:

- veri toplar
- NLP ile bilgi çıkarır
- basit ama açıklanabilir bir ML yaklaşımı uygular
- sonuçları modern bir arayüzde sunar

---

## 2. Ürün Vizyonu

Arayüz ve ürün deneyimi şu hissi vermek üzere yeniden tasarlanmıştır:

- premium AI recruitment platform
- modern startup SaaS dashboard
- enterprise HR analytics system

UI/UX tarafında hedeflenen kalite:

- temiz ve dengeli spacing
- sabit ve kaymayan layout
- dark/light theme desteği
- profesyonel kart yapıları
- güçlü görsel hiyerarşi
- dashboard kalitesinde analitik ekranlar
- canlı sunumda güven veren bir ürün algısı

---

## 3. Temel Özellikler

### Aday / CV İşlemleri

- PDF formatında CV yükleme
- CV’den isim, email, telefon, eğitim, deneyim yılı ve skill çıkarma
- skill’leri normalize ederek veritabanına yazma
- yüklenen adayın tüm iş ilanlarıyla otomatik eşleşmesini görme

### İş İlanı Yönetimi

- yeni iş ilanı oluşturma
- required skill listesi ekleme / çıkarma
- minimum deneyim ve eğitim seviyesi tanımlama
- iş ilanı bazlı aday eşleştirme çalıştırma

### Matching / AI Eşleştirme

- job-to-candidate matching
- candidate-to-all-jobs matching
- weighted scoring ile final match score üretme
- matched skills / missing skills gösterimi
- açıklanabilir skor kırılımı

### Dashboard / Analytics

- toplam aday sayısı
- aktif iş ilanı sayısı
- ortalama eşleşme skoru
- en iyi adaylar
- skill distribution
- score distribution
- aday deneyim dağılımı
- job education dağılımı

### Tasarım ve Deneyim

- TypeScript tabanlı modern frontend mimarisi
- fixed sidebar + sticky topbar
- dark mode / light mode
- localStorage ile persistent theme
- responsive grid sistemi
- loading skeletons
- subtle animations
- enterprise-grade kart yapıları

---

## 4. Sistem Akışı

Projeyi ürün akışı açısından en doğru şekilde şu sırayla düşünebilirsin:

### Akış 1: Job-first yaklaşımı

1. Kullanıcı sisteme girer
2. `Job Postings` sayfasından iş ilanı oluşturur
3. İş ilanına required skills, min experience ve education level ekler
4. `Run Matching` ile sistem tüm adayları bu iş ilanına göre skorlar
5. `Matching` sayfasında aday sıralaması ve AI insights görülür

### Akış 2: Candidate-first yaklaşımı

1. Kullanıcı `CV Upload` sayfasından PDF CV yükler
2. Sistem CV’yi parse eder
3. Aday bilgisi veritabanına kaydedilir
4. Sistem adayı mevcut tüm iş ilanları ile karşılaştırır
5. Kullanıcı aynı anda şunları görebilir:
   - aday profili
   - adayın hangi iş ilanlarına ne kadar uygun olduğu
   - hangi skill’lerin eşleştiği
   - hangi skill’lerin eksik olduğu

### Akış 3: Sunum / Demo akışı

1. Dashboard açılır
2. KPI kartları ve grafikler gösterilir
3. Job posting oluşturulur veya mevcut job seçilir
4. CV yüklenir
5. Candidate profile çıkarılır
6. Matching ekranında sıralama gösterilir
7. AI explanation panel üzerinden neden bu skor verildiği anlatılır

---

## 5. Sayfa Sayfa Sistem Açıklaması

## Dashboard

Dashboard, sistemin yönetim ve sunum giriş ekranıdır.

Bu sayfada gösterilenler:

- total candidates
- active jobs
- average match score
- best candidate
- top skills chart
- score distribution chart
- top candidates listesi
- son oluşturulan job’lar

Amaç:

- sistemin dolu ve çalışan bir ürün olduğunu ilk bakışta göstermek
- canlı sunumda “ürün dashboard’u” hissi vermek
- veri ve görsel kaliteyi aynı anda sunmak

## Candidates

Candidates sayfası aday havuzunu gösterir.

Bu sayfada:

- tüm adaylar tablo halinde listelenir
- adaylar aranabilir
- pagination vardır
- seçilen adayın detay profili sağ panelde gösterilir
- education, experience, skills bilgisi görülebilir
- seçilen adayın tüm job’lara karşı geçmiş match sonuçları görüntülenebilir
- gerekirse aday bazlı matching tekrar çalıştırılabilir

Amaç:

- “Sisteme CV ekleyebiliyoruz” kısmını somutlaştırmak
- “Bu aday hangi işlere ne kadar uyuyor?” sorusunu cevaplamak

## Job Postings

Job Postings sayfası iş ilanı oluşturma ve yönetme ekranıdır.

Bu sayfada:

- job title girilir
- description yazılır
- minimum experience belirlenir
- education level seçilir
- required skill listesi tanımlanır
- suggested skills üzerinden hızlı skill eklenebilir
- oluşturulan job kartları listelenir
- her job için ayrı ayrı matching çalıştırılabilir

Amaç:

- HR tarafının ihtiyaç duyduğu role tanımı akışını göstermek
- eşleştirme motorunu besleyecek giriş verisini üretmek

## Matching

Matching sayfası sistemin en kritik ekranlarından biridir.

Bu sayfada:

- seçilen iş ilanı için aday sıralaması gösterilir
- rank numarası gösterilir
- final score ring gösterilir
- skill / experience / education / semantic score breakdown görünür
- matched skills ve missing skills kartları görünür
- AI Insights panelinde açıklama sunulur
- detay explanation modal ile daha kapsamlı açıklama açılabilir

Amaç:

- yapay zeka eşleştirme mantığını görünür yapmak
- “neden bu aday öne çıktı?” sorusunu açıklamak
- sunumdaki en güçlü teknik ekranı sunmak

## CV Upload

CV Upload sayfası aday onboarding ekranıdır.

Bu sayfada:

- PDF drag & drop alanı vardır
- upload progress gösterilir
- parsing aşamaları adım adım görünür
- extracted candidate profile gösterilir
- candidate’ın en iyi job match sonuçları anında listelenir

Bu sayfa özellikle şu gereksinimi karşılar:

> Sisteme CV ekleyebilelim ve CV eklediğimizde iş ilanıyla ne kadar eşleştiğini görelim.

Amaç:

- en etkileyici demo anını üretmek
- CV yükleme sonrası sistemin gerçekten “akıllı” davrandığını göstermek

## Analytics

Analytics sayfası daha veri odaklı içgörü ekranıdır.

Bu sayfada:

- top skills dağılımı
- score distribution trend
- experience band analizi
- job education requirement dağılımı
- best candidates overview

Amaç:

- sistemin sadece CRUD olmadığını göstermek
- karar destek / analitik yönünü sunmak

## Settings

Settings sayfası ürünün teknik ve sunumsal anlatım ekranıdır.

Bu sayfada:

- theme kontrolü
- scoring formula özeti
- academic architecture özeti
- demo checklist
- kullanılan teknoloji profili

Amaç:

- proje mantığını anlaşılır hale getirmek
- sunum sırasında teknik yapı taşlarını tek ekranda göstermek

---

## 6. Kullanılan Teknolojiler

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Radix UI tabanlı shadcn-style component yapısı
- Framer Motion
- Recharts
- Lucide React
- next-themes

## Backend

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- python-multipart

## NLP / ML Pipeline

- spaCy
- NLTK
- scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- Weighted Scoring

## Geliştirme Yaklaşımı

- modular component architecture
- reusable UI primitives
- local-first architecture
- explainable ML pipeline
- academic-demo friendly system design

---

## 7. Matching Mantığı

Sistemde ağır deep learning modelleri kullanılmaz.

Bunun yerine akademik sunum için daha anlaşılır ve lokal ortamda daha stabil çalışan şu yaklaşım kullanılır:

- skill extraction
- text preprocessing
- TF-IDF vectorization
- cosine similarity
- weighted score calculation

### Final Match Score Formülü

```text
Final Match Score =
40% Skill Match +
30% Experience Match +
20% Education Match +
10% Semantic Similarity
```

### Score Açıklaması

- `Skill Match`: adayın sahip olduğu skill’lerin required skills ile kesişim oranı
- `Experience Match`: aday deneyim yılı / istenen deneyim oranı
- `Education Match`: aday eğitim seviyesi ile job requirement uyumu
- `Semantic Similarity`: CV metni ile job description metni arasındaki TF-IDF + cosine similarity benzerliği

### Açıklanabilirlik

Sistem sadece final score vermez.

Ayrıca:

- matched skills
- missing skills
- alt skorlar
- recommendation text

üretir.

Bu sayede karar verme mantığı daha anlaşılır hale gelir.

---

## 8. Veri Seti ve Veri Hazırlama Yaklaşımı

Proje, büyük ölçekli production dataset yerine küçük ve kontrollü bir akademik demo dataset’i kullanır.

### Resume Dataset

Yaklaşık 100 resume / CV

Örnek kategoriler:

- Python Developer
- Frontend Developer
- Full Stack Developer
- Data Analyst
- Data Scientist
- Machine Learning Engineer
- DevOps Engineer
- Java Developer
- UI/UX Designer

### Job Posting Dataset

Yaklaşık 20 job posting

Örnek roller:

- Senior Python Developer
- Junior Frontend Developer
- Data Analyst
- ML Engineer
- DevOps Specialist
- Full Stack Developer
- Backend Engineer
- React Developer
- AI Engineer
- Cloud Engineer

### Veri Hazırlama Mantığı

- küçük ama kontrollü dataset
- demo sırasında hızlı sonuç
- daha az hata yüzeyi
- daha anlaşılır skor mantığı
- daha yüksek sunum güvenilirliği

---

## 9. Proje Dizini

```text
smart-cv-matcher/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── main.py
│   ├── sample_data/
│   ├── requirements.txt
│   ├── seed_data.py
│   └── smart_cv_matcher.db
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   │   ├── dashboard/
│   │   │   ├── layout/
│   │   │   ├── matching/
│   │   │   └── ui/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── pages/
│   │   ├── types/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   └── tsconfig.json
├── .gitignore
└── README.md
```

---

## 10. Kurulum Ön Koşulları

Projeyi çalıştırmadan önce sisteminde şunların kurulu olması gerekir:

- Python 3.11+ veya uyumlu bir Python 3 sürümü
- Node.js 20+
- npm

Not:

- Backend FastAPI ile `8000` portunda çalışır
- Frontend Vite ile `5173` portunda çalışır
- Frontend `/api` isteklerini otomatik olarak backend’e proxy eder

---

## 11. Projeyi İlk Kurulumda Çalıştırma

Bu komutlar sıfırdan kurulum içindir.

## Terminal 1 — Backend

```bash
cd /Users/samet/Desktop/datawarehouse/smart-cv-matcher/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python seed_data.py
python -m uvicorn app.main:app --reload --port 8000
```

## Terminal 2 — Frontend

```bash
cd /Users/samet/Desktop/datawarehouse/smart-cv-matcher/frontend
npm install
npm run dev
```

Ardından tarayıcıda aç:

```text
http://127.0.0.1:5173
```

Backend health check:

```text
http://127.0.0.1:8000/api/health
```

Backend Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

## 12. Günlük Kullanımda Projeyi Çalıştırma

Bağımlılıklar zaten kuruluysa daha kısa komutlar yeterlidir.

## Terminal 1 — Backend

```bash
cd /Users/samet/Desktop/datawarehouse/smart-cv-matcher/backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

## Terminal 2 — Frontend

```bash
cd /Users/samet/Desktop/datawarehouse/smart-cv-matcher/frontend
npm run dev
```

---

## 13. Demo Senaryosu

Canlı sunum için önerilen akış:

1. `Dashboard` aç
2. KPI kartları ve grafiklerle sistemi tanıt
3. `Job Postings` sayfasına geç
4. Hazır job’lardan birini göster veya yeni job oluştur
5. `CV Upload` sayfasından bir CV yükle
6. Çıkan candidate profile’ı göster
7. Aynı CV’nin sistemdeki job’larla ne kadar eşleştiğini göster
8. `Matching` sayfasında job bazlı aday sıralamasını göster
9. `AI Insights` panelini aç ve skorun neden üretildiğini anlat
10. `Analytics` sayfasında sistemin veri yönünü göster

---

## 14. API Özeti

Sistemde öne çıkan endpoint’ler:

### Candidate

- `POST /api/candidates/upload`
- `GET /api/candidates`
- `GET /api/candidates/{candidate_id}`
- `DELETE /api/candidates/{candidate_id}`

### Jobs

- `POST /api/jobs`
- `GET /api/jobs`
- `GET /api/jobs/{job_id}`
- `DELETE /api/jobs/{job_id}`

### Matching

- `POST /api/match/{job_id}`
- `GET /api/match/{job_id}/results`
- `GET /api/match/explain/{match_id}`
- `POST /api/match/candidate/{candidate_id}`
- `GET /api/match/candidate/{candidate_id}/results`

### Analytics

- `GET /api/analytics/dashboard`

---

## 15. Mevcut Başarı Durumu

Bu proje şu anda aşağıdaki hedefleri başarılı şekilde karşılamaktadır:

- CV yükleme çalışıyor
- PDF parse akışı çalışıyor
- aday bilgisi çıkarılıyor
- skill extraction çalışıyor
- job oluşturma çalışıyor
- job bazlı matching çalışıyor
- candidate bazlı all-job matching çalışıyor
- AI explanation panel çalışıyor
- dashboard ve analytics görselleştirmeleri çalışıyor
- dark/light theme çalışıyor
- responsive SaaS layout çalışıyor
- frontend build başarılı

Özetle:

Bu sistem artık hem teknik akış hem de ürün görünümü açısından sunulabilir seviyededir.

---

## 16. Tasarım ve UI/UX Notları

Yeni frontend aşağıdaki tasarım prensiplerine göre kurulmuştur:

- fixed sidebar
- sticky topbar
- stable container sizing
- responsive dashboard sections
- modern SaaS card language
- consistent radius and spacing system
- premium dark/light themes
- polished charts and ranking cards
- page-level transitions
- loading skeletons

Bu sayede önceki sürümde görülen şu sorunlar önemli ölçüde giderilmiştir:

- layout kaymaları
- düzensiz spacing
- zayıf görsel hiyerarşi
- eski admin panel hissi
- responsive bozulmalar
- zayıf dashboard estetiği

---

## 17. Bilinen Sınırlar

Bu proje bilinçli olarak bazı sınırlar içinde tutulmuştur:

- büyük ölçekli production ATS değildir
- gerçek zamanlı çok kullanıcılı sistem değildir
- büyük LLM tabanlı semantic engine kullanmaz
- enterprise infra, queue, worker, auth, RBAC gibi katmanları içermez

Bunlar eksiklik değil, proje hedefinin akademik demo olması nedeniyle bilinçli tasarım tercihleridir.

---

## 18. Geliştirme Notları

Frontend tarafında öne çıkan mimari kararlar:

- eski JSX yapı TypeScript tabanlı yapıya taşındı
- ortak reusable UI bileşenleri oluşturuldu
- layout shell merkezi hale getirildi
- sayfalar lazy-load edildi
- theme management eklendi

Backend tarafında öne çıkan geliştirme:

- candidate-to-all-jobs matching endpoint’leri eklendi
- böylece yüklenen adayın tüm iş ilanlarıyla ne kadar eşleştiği gösterilebilir hale geldi

---

## 19. Kısa Sonuç

SmartCV, açıklanabilir NLP/ML pipeline ile modern SaaS dashboard deneyimini bir araya getiren, lokal ortamda çalışan, sunum odaklı bir AI recruitment platform prototype’ıdır.

Bu proje özellikle şu mesajı vermek için uygundur:

> “Bu sadece bir okul ödevi ekranı değil; gerçek bir AI recruitment startup ürününün güçlü bir prototipi.”
