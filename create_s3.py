import boto3
import os
from dotenv import load_dotenv

load_dotenv()
aws_access_key=os.getenv("AWS_ACCESS_KEY")
aws_secret_key=os.getenv("AWS_SECRET_KEY")
aws_region=os.getenv("AWS_REGION")
BUCKET_NAME="olist-project-bucket"


def create_s3_client():
    s3_client=boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
       
    )
    try:
        s3_client.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={
                "LocationConstraint":aws_region
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
    
    

  
            





