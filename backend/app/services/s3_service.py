import boto3
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def generate_s3_key(filename: str, folder: str = "pdfs") -> tuple:
    """
    Generate organized S3 key with date-based structure.
    
    Args:
        filename: Original filename
        folder: Folder type (pdfs, testcases)
        
    Returns:
        tuple of (s3_key, file_id)
    """
    now = datetime.now()
    file_id = str(uuid.uuid4())
    
    # Clean filename
    clean_filename = filename.replace(" ", "_")
    
    # Create key: folder/YYYY/MM/DD/uuid-filename
    s3_key = f"{folder}/{now.year}/{now.month:02d}/{now.day:02d}/{file_id}-{clean_filename}"
    
    return s3_key, file_id


def upload_pdf_to_s3(file_bytes: bytes, filename: str) -> dict:
    """
    Upload PDF file to S3.
    
    Args:
        file_bytes: PDF file content as bytes
        filename: Original filename
        
    Returns:
        dict with s3_key, file_id, and s3_url
    """
    try:
        s3_key, file_id = generate_s3_key(filename, "pdfs")
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_bytes,
            ContentType='application/pdf',
            Metadata={
                'original-filename': filename,
                'uploaded-at': datetime.now().isoformat()
            }
        )
        
        # Generate S3 URL
        s3_url = f"s3://{S3_BUCKET_NAME}/{s3_key}"
        
        return {
            "success": True,
            "s3_key": s3_key,
            "file_id": file_id,
            "s3_url": s3_url
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to upload PDF to S3: {str(e)}"
        }


def upload_testcases_to_s3(test_cases: dict, filename: str, file_id: str, format_type: str = "json") -> dict:
    """
    Upload generated test cases to S3.
    
    Args:
        test_cases: Test case data
        filename: Original PDF filename
        file_id: UUID for this upload session
        format_type: 'json' or 'markdown'
        
    Returns:
        dict with s3_key and s3_url
    """
    try:
        # Prepare filename
        base_name = filename.replace('.pdf', '')
        extension = 'json' if format_type == 'json' else 'md'
        test_filename = f"{base_name}-testcases.{extension}"
        
        # Generate S3 key with same file_id
        now = datetime.now()
        s3_key = f"testcases/{now.year}/{now.month:02d}/{now.day:02d}/{file_id}-{test_filename}"
        
        # Prepare content
        if format_type == 'json':
            import json
            content = json.dumps(test_cases, indent=2)
            content_type = 'application/json'
        else:  # markdown
            content = test_cases.get('text', str(test_cases))
            content_type = 'text/markdown'
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=content.encode('utf-8'),
            ContentType=content_type,
            Metadata={
                'original-pdf': filename,
                'generated-at': datetime.now().isoformat()
            }
        )
        
        s3_url = f"s3://{S3_BUCKET_NAME}/{s3_key}"
        
        return {
            "success": True,
            "s3_key": s3_key,
            "s3_url": s3_url
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to upload test cases to S3: {str(e)}"
        }


def get_file_from_s3(s3_key: str) -> dict:
    """
    Download file from S3.
    
    Args:
        s3_key: S3 object key
        
    Returns:
        dict with file content and metadata
    """
    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key
        )
        
        content = response['Body'].read()
        
        return {
            "success": True,
            "content": content,
            "content_type": response.get('ContentType'),
            "metadata": response.get('Metadata', {})
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to download from S3: {str(e)}"
        }


def list_files_from_s3(prefix: str = "", max_items: int = 100) -> dict:
    """
    List files from S3 bucket.
    
    Args:
        prefix: Folder prefix to filter (e.g., 'pdfs/', 'testcases/')
        max_items: Maximum number of items to return
        
    Returns:
        dict with list of files
    """
    try:
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET_NAME,
            Prefix=prefix,
            MaxKeys=max_items
        )
        
        files = []
        for obj in response.get('Contents', []):
            files.append({
                "key": obj['Key'],
                "size": obj['Size'],
                "last_modified": obj['LastModified'].isoformat()
            })
        
        return {
            "success": True,
            "files": files,
            "count": len(files)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list S3 files: {str(e)}"
        }


def test_s3_connection() -> bool:
    """
    Test S3 connection and bucket access.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        s3_client.head_bucket(Bucket=S3_BUCKET_NAME)
        print(f"✅ S3 connection successful! Bucket: {S3_BUCKET_NAME}")
        return True
    except Exception as e:
        print(f"❌ S3 connection failed: {str(e)}")
        return False
