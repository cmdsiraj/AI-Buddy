import os
from io import BytesIO
import boto3
from botocore.client import Config
from dotenv import load_dotenv

# .env keys:
# CF_ACCOUNT_ID=...
# CF_ACCESS_KEY=...
# CF_SECRET_KEY=...
# BUCKET=...

def setup_connection():
    load_dotenv()
    ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
    ACCESS_KEY = os.getenv("CF_ACCESS_KEY")
    SECRET_KEY = os.getenv("CF_SECRET_KEY")

    # Debug (safe): print only account id, never secrets
    print("R2 Account:", ACCOUNT_ID)

    return boto3.client(
        "s3",
        endpoint_url=f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="auto",
    )

def save_pdf(buf: BytesIO, file_name: str, file_type: str, file_id: str):
    """Upload a PDF (in-memory buffer) to R2 and return a presigned download URL."""
    try:
        load_dotenv()
        BUCKET = os.getenv("BUCKET")
        s3 = setup_connection()

        # Make sure buffer is at start
        buf.seek(0)

        # 'file_id' is the object key/path in the bucket (e.g., "pdfs/123/report.pdf")
        key = str(file_id)

        print("Uploading to:", BUCKET, key)

        s3.put_object(
            Bucket=BUCKET,                # <-- capitalized
            Key=key,                      # <-- capitalized
            Body=buf.getvalue(),
            ContentType=f"application/{file_type}",  # e.g., "application/pdf"
            ContentDisposition=f'inline; filename="{file_name}"'
        )

        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET, "Key": key},   # <-- capitalized
            ExpiresIn=3600
        )

        return {"bucket": BUCKET, "key": key, "download_url": url}

    except Exception as e:
        raise Exception(f"PDF Upload Failed: {e}")
