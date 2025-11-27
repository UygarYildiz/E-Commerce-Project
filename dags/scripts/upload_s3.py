import boto3
import os
from dotenv import load_dotenv
import sys
load_dotenv()


# .envden bucket ismini almak için
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# S3e dosya yükleme fonksiyonu
def upload_to_s3():
    if not BUCKET_NAME:
        print("HATA: AWS_BUCKET_NAME .env dosyasında tanımlı değil")
        raise ValueError("AWS_BUCKET_NAME .env dosyasında tanımlı değil")
    s3_client=boto3.client("s3")

    data_folder="/opt/airflow/data/raw"
    if not os.path.exists(data_folder):
        print(f"HATA Klasör bulunamadı {data_folder}")
        raise FileNotFoundError(f" Klasör yok: {data_folder}")
        
        
    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):
            file_path=os.path.join(data_folder,filename)
            s3_path=f"raw/{filename}"
            print(f" Dosya yükleniyor:{file_path} --> s3://{BUCKET_NAME}/{s3_path}")

            try:
                s3_client.upload_file(file_path,BUCKET_NAME,s3_path)
                print(f" Yükleme başarılı: {filename} dosyası S3'e {s3_path}'e yüklendi.")
            except Exception as e:
                print(f" {filename} dosyası S3'e yüklenemedi :{e}")
                raise e
            

   

            
        





                 
