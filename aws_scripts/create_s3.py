import boto3
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME="olist-project-bucket"
default_region="eu-central-1"

def create_s3_client():
    s3_client=boto3.client(
        "s3"
    )
    try:
        s3_client.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={
                "LocationConstraint":default_region
            }
        )
        print(f"Bucket oluşturuldu: {BUCKET_NAME}")
    except Exception as e:
        print(f"Hata oluştu: {e}"

        )
    folders=["raw/","processed/"]

    for folder in folders:
        s3_client.put_object(Bucket=BUCKET_NAME,Key=folder)
        print(f"Klasör oluşturuldu: {folder}")  
    

if __name__=="__main__":
    create_s3_client()   
    
    

  
            





