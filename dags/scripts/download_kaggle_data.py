import os
from dotenv import load_dotenv
load_dotenv()
from kaggle.api.kaggle_api_extended import KaggleApi

def download_kaggle_dataset():
    # Kaggle API'ye kimlik doğrulama
    api = KaggleApi()
    api.authenticate()


    # İndirilecek veri seti
    dataset="olistbr/brazilian-ecommerce"

    #Hedef dizin
    target_path="/opt/airflow/data/raw"

    # Klasör yoksa oluştur
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    print(f"Veri seti indiriliyor: {dataset} dizinine: {target_path}")


    # Veri setini indir ve aç

    print(f"Veri seti indiriliyor: {dataset} -> {target_path}")

    api.dataset_download_files(dataset,
                               path=target_path,
                               unzip=True)
    
    print("Veri seti indirildi ve açıldı.")


    print("İndirme tamamlandı.")






