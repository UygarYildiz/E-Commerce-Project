import re
import boto3
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,text

load_dotenv()

# Konfigürasyonlar
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
BUCKET_NAME=os.getenv("AWS_BUCKET_NAME")


# RDS connection stringi
CONN_STRING=f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


#Tablo isimlerini çıkarmak için fonksiyonumuz
def extract_table_name(file_key):

    filename=file_key.split("/")[-1]

    return filename.replace("_dataset.csv","").replace(".csv","")




def load_to_rds():
    #s3 clienti oluşturmak için
    engine=create_engine(CONN_STRING)
    s3_client=boto3.client("s3")

    # Aşağıdaaki döngüyü gereksiz şekilde çalıştırmamak için RDS bağlantısı kontrolü
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT version()"))
            print(" Bağlantı başarılı")
    except Exception as e:
            print(f"RDS bağlantı hatası {e}")
            raise


    # Raw dataları listeliyoruz ve list_response değişkenine atıyoruz.
    list_response=s3_client.list_objects_v2(Bucket=BUCKET_NAME,Prefix="raw/")

    #Burada Conent içerisindeki csv dosyalarını alıyoruz.
    csv_files=[
        obj for obj in list_response.get("Contents",[]) 
        if obj["Key"].endswith(".csv")]


    # Eğer csv_files içeriisnde dosya yoksa raw/ klasöründ .csv olmadığından hata fırlatıyoruz.
    if not csv_files:
        raise ValueError("raw/ klasöründe CSV dosyası bulunamadı!")

    print("Bulunan dosyalar")
    print(f"{len(csv_files)} adet CSV dosyası bulundu")


    for obj in csv_files:
        
        file_keys=obj["Key"]
        table_name=extract_table_name(file_keys)
        response=s3_client.get_object(Bucket=BUCKET_NAME,Key=file_keys)
        df=pd.read_csv(response["Body"])

        print(f"{file_keys} dosyası okundu {len(df)} satır {len(df.columns)} sütün")
        try:
            with engine.begin() as conn:
                conn.execute(text(f"TRUNCATE TABLE {table_name}"))

                df.to_sql(
                    table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    method="multi",
                    chunksize=5000
                    )
                
            print(f"{table_name} yüklendi")
        except Exception as e:
            print(f"    {table_name} yüklenemedi: {e}")
            print(f"    Hata tipi: {type(e).__name__}")
            print(f"   Hata mesajı: {str(e)[:500]}")
            print(f"    DataFrame info:")
            print(df.info())

if __name__ =="__main__":
    load_to_rds()


    


        













