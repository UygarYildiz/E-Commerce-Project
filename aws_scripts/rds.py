import boto3
import os
from dotenv import load_dotenv
load_dotenv()




def create_rds_instance():
    rds=boto3.client("rds")

    db_identifier="olist-database"
    db_name="olist"

    master_username=os.getenv("DB_USER","postgres_admin")
    master_password=os.getenv("DB_PASSWORD")

    try:
        response=rds.create_db_instance(
            DBNAME=db_name,
            DBInstanceIdentifier=db_identifier,
            AllocatedStorage=4,
            DBInstanceClass="db.t3.micro",
            Engine="postgres",
            MasterUsername=master_username,
            MasterUserPassword=master_password,
            PubliclyAccessible=True,
            MultiAZ=False,
            StorageType="gp2",
            BackupRetentionPeriod=1,
            Tags=[{"Key":"Project","Value":"Olist-ETL"}]
        )

        print("Veritabanı başarıyla oluşturuldu.")
        
    except Exception as e:
        print(f"RDS oluşturulurken hata oluştu: {e}")
    
if __name__=="__main__":
    create_rds_instance()