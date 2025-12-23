import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = "testcaseai-pdf-storage"

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def upload_pdf_to_s3(file_bytes: bytes, filename: str, file_id: str) -> dict:
    """
    Upload PDF file to S3.
    
    Args:
        file_bytes: PDF file content as bytes
        filename: Original filename
        file_id: Unique file identifier
        
    Returns:
        dict with success status and S3 URL
    """
    try:
        # Create folder structure by date
        today = datetime.now().strftime("%Y-%m-%d")
        s3_key = f"pdfs/{today}/{file_id}_{filename}"
        
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
        
        s3_url = f"s3://{S3_BUCKET_NAME}/{s3_key}"
        
        return {
            "success": True,
            "s3_url": s3_url,
            "s3_key": s3_key
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to upload PDF to S3: {str(e)}"
        }


def upload_testcases_to_s3(testcases_data: dict, original_filename: str, file_id: str, format_type: str = "json") -> dict:
    """
    Upload generated test cases to S3.
    
    Args:
        testcases_data: Test cases data from Gemini
        original_filename: Original PDF filename
        file_id: Unique file identifier
        format_type: Format type ('json' or 'markdown')
        
    Returns:
        dict with success status and S3 URL
    """
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        
        if format_type == "json":
            # Save as JSON
            import json
            content = json.dumps(testcases_data, indent=2)
            s3_key = f"testcases/{today}/{file_id}_testcases.json"
            content_type = "application/json"
        else:  # markdown
            # Save as Markdown
            content = testcases_data.get("text", "No test cases generated")
            s3_key = f"testcases/{today}/{file_id}_testcases.md"
            content_type = "text/markdown"
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key,
            Body=content.encode('utf-8'),
            ContentType=content_type,
            Metadata={
                'original-filename': original_filename,
                'file-id': file_id,
                'format': format_type,
                'created-at': datetime.now().isoformat()
            }
        )
        
        s3_url = f"s3://{S3_BUCKET_NAME}/{s3_key}"
        
        return {
            "success": True,
            "s3_url": s3_url,
            "s3_key": s3_key,
            "format": format_type
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
        dict with file content or error
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
            "content_type": response.get('ContentType', 'application/octet-stream')
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to download file from S3: {str(e)}"
        }


def list_files_from_s3(prefix: str = "") -> dict:
    """
    List files from S3 bucket.
    
    Args:
        prefix: Optional prefix to filter files
        
    Returns:
        dict with list of files
    """
    try:
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET_NAME,
            Prefix=prefix
        )
        
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat()
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


def delete_file_from_s3(s3_key: str) -> dict:
    """
    Delete a file from S3.
    
    Args:
        s3_key: S3 object key
        
    Returns:
        dict with success status
    """
    try:
        s3_client.delete_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_key
        )
        
        return {
            "success": True,
            "message": f"File deleted from S3: {s3_key}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete file from S3: {str(e)}"
        }
