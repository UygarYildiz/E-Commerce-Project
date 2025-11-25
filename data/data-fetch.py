import os
from dotenv import load_dotenv
load_dotenv()
from kaggle.api.kaggle_api_extended import KaggleApi

def download_kaggle_dataset():
    # Kaggle API'ye kimlik doğrulama
    api = KaggleApi()
    api.authenticate()

    dataset="olistbr/brazilian-ecommerce"

    #Hedef dizin
    target_path=os.path.join(os.getcwd(),"data","raw")

    # Klasör yoksa oluştur
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    print(f"Veri seti indiriliyor: {dataset} dizinine: {target_path}")

    # Veri setini indir ve aç

    api.dataset_download_files(dataset,
                               path=target_path,
                               unzip=True)
    
    print("Veri seti indirildi ve açıldı.")


    print("İndirme tamamlandı.")

if __name__=="__main__":
     download_kaggle_dataset()




