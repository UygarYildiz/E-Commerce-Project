# End-to-End E-Ticaret Veri Mühendisliği Projesi

Bu proje, ham e-ticaret verilerini işlenebilir içgörülere dönüştüren modern bir veri boru hattı (pipeline) oluşturmayı amaçlar.

**Kullanılan Teknolojiler:** Python, SQL, AWS (S3, RDS), Airflow, dbt.
**Veri Seti:** [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## Faz 0: Hazırlık ve Kurulum

Projeye başlamadan önce ortamı hazırlamalıyız.

1.  **AWS Hesabı:** AWS Free Tier (Ücretsiz Katman) hesabı oluştur.
2.  **Kaggle API:** Veriyi indirmek için Kaggle API token'ını (`kaggle.json`) al.
3.  **Lokal Ortam:**
    *   VS Code'da proje klasörünü aç.
    *   Python sanal ortamı (virtual environment) oluştur (`python -m venv venv`).
    *   Docker Desktop'ı kur (Airflow için gerekli olacak).
    *   Git reposu başlat (`git init`).

---

## Faz 1: AWS Altyapısı (Infrastructure)

Bulut kaynaklarını manuel veya kod ile oluşturma aşaması.

1.  **IAM Kullanıcısı:** Root hesabı kullanma. `AdministratorAccess` veya sadece S3/RDS yetkisi olan bir IAM kullanıcısı oluştur ve `Access Key` / `Secret Key` bilgilerini not et.
2.  **S3 Bucket (Data Lake):**
    *   `olist-project-raw-data` (isim benzersiz olmalı) adında bir bucket oluştur.
    *   Klasör yapısını kafanda kur: `raw/`, `processed/`.
3.  **RDS PostgreSQL (Data Warehouse):**
    *   AWS RDS servisinde "Free Tier" seçeneğiyle bir PostgreSQL veritabanı oluştur.
    *   **Önemli:** "Publicly Accessible" seçeneğini 'Yes' yap (lokalden bağlanabilmek için).
    *   Güvenlik Grubu (Security Group) ayarlarından kendi IP adresine gelen trafiğe izin ver.

*   **Öğrenilecek Kavramlar:** IAM Rolleri, S3 Storage Classes, Security Groups, VPC (Temel seviye).

---

## Faz 2: Veri Alımı (Ingestion - Python)

Veriyi Kaggle'dan alıp S3'e yükleyen Python scriptlerinin yazılması.

1.  **Veriyi İndirme:** `kaggle` kütüphanesini kullanarak veriyi `data/` klasörüne indiren bir script yaz.
2.  **S3'e Yükleme:** `boto3` kütüphanesini kullanarak `data/` içindeki CSV dosyalarını S3 bucket'ındaki `raw/` klasörüne yükle.
3.  **Güvenlik:** AWS şifrelerini asla koda gömme! `.env` dosyası kullan ve `python-dotenv` kütüphanesi ile çek.

*   **Kod İpucu:** `s3_client.upload_file(local_path, bucket_name, s3_path)`
*   **Öğrenilecek Kavramlar:** Boto3 SDK, Environment Variables, Python File I/O.

---

## Faz 3: Orkestrasyon (Airflow)

Süreci otomatize etme. Scriptleri elle çalıştırmak yerine Airflow yönetecek.

1.  **Airflow Kurulumu:** Docker kullanarak Airflow'u ayağa kaldır (Resmi docker-compose dosyasını kullanabilirsin).
2.  **DAG Oluşturma:** `etl_pipeline` adında bir DAG (Directed Acyclic Graph) oluştur.
3.  **Task Tanımlama:**
    *   `Task 1`: Veriyi indir (PythonOperator veya BashOperator).
    *   `Task 2`: Veriyi S3'e yükle (PythonOperator).
4.  **Zamanlama:** DAG'ı günde bir kez çalışacak şekilde ayarla (`schedule_interval='@daily'`).

*   **Kod İpucu:** `default_args` içinde `retries` tanımlamayı unutma.
*   **Öğrenilecek Kavramlar:** DAG yapısı, Operators, XComs (Taskler arası veri paylaşımı), Docker Container mantığı.

---

## Faz 4: Veri Yükleme (Loading - S3 to RDS)

Veriyi S3'ten alıp veritabanına "Ham" (Raw) tablolar olarak yükleme.

1.  **Veritabanı Bağlantısı:** DBeaver veya pgAdmin ile RDS'e bağlan.
2.  **Tablo Oluşturma (DDL):** CSV dosyalarındaki sütunlara uygun `CREATE TABLE` komutlarını yaz (örn: `raw_orders`, `raw_customers`). Veri tiplerine dikkat et (VARCHAR, INT, TIMESTAMP).
3.  **Veri Aktarımı:**
    *   Bunu Airflow'da yeni bir Task olarak ekle.
    *   Python `pandas` kullanarak CSV'yi oku ve `sqlalchemy` ile veritabanına yaz (`to_sql` metodu).
    *   *Alternatif (Daha İleri Seviye):* AWS S3'ten direkt RDS'e `COPY` komutu ile yükleme (aws_s3 extension gerekebilir).

*   **Öğrenilecek Kavramlar:** DDL vs DML, SQLAlchemy Engine, Bulk Insert performansı.

---

## Faz 5: Veri Dönüşümü ve Modelleme (dbt)

Projenin kalbi. Ham veriyi anlamlı iş verisine dönüştürme.

1.  **dbt Kurulumu:** `dbt-core` ve `dbt-postgres` paketlerini kur. `dbt init` ile projeyi başlat.
2.  **Profiles.yml:** RDS bağlantı bilgilerini `profiles.yml` dosyasına gir.
3.  **Sources:** `models/staging/sources.yml` dosyasında ham tablolarını (raw_orders vb.) tanımla.
4.  **Staging Models:** Ham veriyi temizle. Sütun isimlerini düzelt, tarih formatlarını ayarla. (Örn: `stg_orders.sql`).
5.  **Dimensional Modeling (Star Schema):**
    *   **Fact Table:** `fct_orders` (Sipariş ID, Müşteri ID, Tutar, Tarih).
    *   **Dim Tables:** `dim_customers` (Müşteri detayları), `dim_products` (Ürün kategorileri).
6.  **Testler:** `schema.yml` dosyasında `unique` ve `not_null` testlerini tanımla.

*   **Kod İpucu:** SQL dosyalarında `SELECT ... FROM {{ source('raw', 'orders') }}` yapısını kullan.
*   **Öğrenilecek Kavramlar:** Star Schema, Normalization, CTE (Common Table Expressions), Data Lineage.

---

## Faz 6: Final ve Sunum

1.  **Dokümantasyon:** `dbt docs generate` ve `dbt docs serve` komutları ile veri sözlüğünü oluştur.
2.  **Görselleştirme (Opsiyonel):** Metabase veya Google Looker Studio'yu RDS'e bağla. "Hangi kategoride en çok satış yapıldı?", "Aylık ciro nedir?" gibi soruların grafiklerini çiz.
3.  **Github:** Kodlarını Github'a yükle. `README.md` dosyanı proje mimarisini anlatacak şekilde düzenle.

---

**Başarılar!** Bu projeyi tamamladığında Junior seviyesinin çok üzerinde bir yetkinliğe ulaşmış olacaksın// filepath: c:\Users\uygar\Desktop\CV_Proje\PROJECT_PLAN.md
# End-to-End E-Ticaret Veri Mühendisliği Projesi

Bu proje, ham e-ticaret verilerini işlenebilir içgörülere dönüştüren modern bir veri boru hattı (pipeline) oluşturmayı amaçlar.

**Kullanılan Teknolojiler:** Python, SQL, AWS (S3, RDS), Airflow, dbt.
**Veri Seti:** [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## Faz 0: Hazırlık ve Kurulum

Projeye başlamadan önce ortamı hazırlamalıyız.

1.  **AWS Hesabı:** AWS Free Tier (Ücretsiz Katman) hesabı oluştur.
2.  **Kaggle API:** Veriyi indirmek için Kaggle API token'ını (`kaggle.json`) al.
3.  **Lokal Ortam:**
    *   VS Code'da proje klasörünü aç.
    *   Python sanal ortamı (virtual environment) oluştur (`python -m venv venv`).
    *   Docker Desktop'ı kur (Airflow için gerekli olacak).
    *   Git reposu başlat (`git init`).

---

## Faz 1: AWS Altyapısı (Infrastructure)

Bulut kaynaklarını manuel veya kod ile oluşturma aşaması.

1.  **IAM Kullanıcısı:** Root hesabı kullanma. `AdministratorAccess` veya sadece S3/RDS yetkisi olan bir IAM kullanıcısı oluştur ve `Access Key` / `Secret Key` bilgilerini not et.
2.  **S3 Bucket (Data Lake):**
    *   `olist-project-raw-data` (isim benzersiz olmalı) adında bir bucket oluştur.
    *   Klasör yapısını kafanda kur: `raw/`, `processed/`.
3.  **RDS PostgreSQL (Data Warehouse):**
    *   AWS RDS servisinde "Free Tier" seçeneğiyle bir PostgreSQL veritabanı oluştur.
    *   **Önemli:** "Publicly Accessible" seçeneğini 'Yes' yap (lokalden bağlanabilmek için).
    *   Güvenlik Grubu (Security Group) ayarlarından kendi IP adresine gelen trafiğe izin ver.

*   **Öğrenilecek Kavramlar:** IAM Rolleri, S3 Storage Classes, Security Groups, VPC (Temel seviye).

---

## Faz 2: Veri Alımı (Ingestion - Python)

Veriyi Kaggle'dan alıp S3'e yükleyen Python scriptlerinin yazılması.

1.  **Veriyi İndirme:** `kaggle` kütüphanesini kullanarak veriyi `data/` klasörüne indiren bir script yaz.
2.  **S3'e Yükleme:** `boto3` kütüphanesini kullanarak `data/` içindeki CSV dosyalarını S3 bucket'ındaki `raw/` klasörüne yükle.
3.  **Güvenlik:** AWS şifrelerini asla koda gömme! `.env` dosyası kullan ve `python-dotenv` kütüphanesi ile çek.

*   **Kod İpucu:** `s3_client.upload_file(local_path, bucket_name, s3_path)`
*   **Öğrenilecek Kavramlar:** Boto3 SDK, Environment Variables, Python File I/O.

---

## Faz 3: Orkestrasyon (Airflow)

Süreci otomatize etme. Scriptleri elle çalıştırmak yerine Airflow yönetecek.

1.  **Airflow Kurulumu:** Docker kullanarak Airflow'u ayağa kaldır (Resmi docker-compose dosyasını kullanabilirsin).
2.  **DAG Oluşturma:** `etl_pipeline` adında bir DAG (Directed Acyclic Graph) oluştur.
3.  **Task Tanımlama:**
    *   `Task 1`: Veriyi indir (PythonOperator veya BashOperator).
    *   `Task 2`: Veriyi S3'e yükle (PythonOperator).
4.  **Zamanlama:** DAG'ı günde bir kez çalışacak şekilde ayarla (`schedule_interval='@daily'`).

*   **Kod İpucu:** `default_args` içinde `retries` tanımlamayı unutma.
*   **Öğrenilecek Kavramlar:** DAG yapısı, Operators, XComs (Taskler arası veri paylaşımı), Docker Container mantığı.

---

## Faz 4: Veri Yükleme (Loading - S3 to RDS)

Veriyi S3'ten alıp veritabanına "Ham" (Raw) tablolar olarak yükleme.

1.  **Veritabanı Bağlantısı:** DBeaver veya pgAdmin ile RDS'e bağlan.
2.  **Tablo Oluşturma (DDL):** CSV dosyalarındaki sütunlara uygun `CREATE TABLE` komutlarını yaz (örn: `raw_orders`, `raw_customers`). Veri tiplerine dikkat et (VARCHAR, INT, TIMESTAMP).
3.  **Veri Aktarımı:**
    *   Bunu Airflow'da yeni bir Task olarak ekle.
    *   Python `pandas` kullanarak CSV'yi oku ve `sqlalchemy` ile veritabanına yaz (`to_sql` metodu).
    *   *Alternatif (Daha İleri Seviye):* AWS S3'ten direkt RDS'e `COPY` komutu ile yükleme (aws_s3 extension gerekebilir).

*   **Öğrenilecek Kavramlar:** DDL vs DML, SQLAlchemy Engine, Bulk Insert performansı.

---

## Faz 5: Veri Dönüşümü ve Modelleme (dbt)

Projenin kalbi. Ham veriyi anlamlı iş verisine dönüştürme.

1.  **dbt Kurulumu:** `dbt-core` ve `dbt-postgres` paketlerini kur. `dbt init` ile projeyi başlat.
2.  **Profiles.yml:** RDS bağlantı bilgilerini `profiles.yml` dosyasına gir.
3.  **Sources:** `models/staging/sources.yml` dosyasında ham tablolarını (raw_orders vb.) tanımla.
4.  **Staging Models:** Ham veriyi temizle. Sütun isimlerini düzelt, tarih formatlarını ayarla. (Örn: `stg_orders.sql`).
5.  **Dimensional Modeling (Star Schema):**
    *   **Fact Table:** `fct_orders` (Sipariş ID, Müşteri ID, Tutar, Tarih).
    *   **Dim Tables:** `dim_customers` (Müşteri detayları), `dim_products` (Ürün kategorileri).
6.  **Testler:** `schema.yml` dosyasında `unique` ve `not_null` testlerini tanımla.

*   **Kod İpucu:** SQL dosyalarında `SELECT ... FROM {{ source('raw', 'orders') }}` yapısını kullan.
*   **Öğrenilecek Kavramlar:** Star Schema, Normalization, CTE (Common Table Expressions), Data Lineage.

---

## Faz 6: Final ve Sunum

1.  **Dokümantasyon:** `dbt docs generate` ve `dbt docs serve` komutları ile veri sözlüğünü oluştur.
2.  **Görselleştirme (Opsiyonel):** Metabase veya Google Looker Studio'yu RDS'e bağla. "Hangi kategoride en çok satış yapıldı?", "Aylık ciro nedir?" gibi soruların grafiklerini çiz.
3.  **Github:** Kodlarını Github'a yükle. `README.md` dosyanı proje mimarisini anlatacak şekilde düzenle.

---

**Başarılar!** Bu projeyi tamamladığında Junior seviyesinin çok üzerinde bir yetkinliğe ulaşmış olacaksın.