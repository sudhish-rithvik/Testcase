import boto3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
DYNAMODB_TABLE_NAME = "TestCaseAI-Metadata"

# Initialize DynamoDB client
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def create_table_if_not_exists():
    """
    Create DynamoDB table if it doesn't exist.
    """
    try:
        dynamodb_client = boto3.client(
            'dynamodb',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        
        # Check if table exists
        try:
            dynamodb_client.describe_table(TableName=DYNAMODB_TABLE_NAME)
            print(f"✅ DynamoDB table already exists: {DYNAMODB_TABLE_NAME}")
            return True
        except dynamodb_client.exceptions.ResourceNotFoundException:
            print(f"Creating DynamoDB table: {DYNAMODB_TABLE_NAME}")
            
            # Create table
            dynamodb_client.create_table(
                TableName=DYNAMODB_TABLE_NAME,
                KeySchema=[
                    {'AttributeName': 'file_id', 'KeyType': 'HASH'}  # Partition key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'file_id', 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'  # On-demand pricing (free tier friendly)
            )
            
            # Wait for table to be active
            print("Waiting for table to become active...")
            waiter = dynamodb_client.get_waiter('table_exists')
            waiter.wait(TableName=DYNAMODB_TABLE_NAME)
            
            print(f"✅ DynamoDB table created: {DYNAMODB_TABLE_NAME}")
            return True
            
    except Exception as e:
        print(f"❌ DynamoDB table creation failed: {str(e)}")
        return False


def save_metadata(file_id: str, metadata: dict) -> dict:
    """
    Save file metadata to DynamoDB.
    
    Args:
        file_id: Unique file identifier
        metadata: Dictionary containing file metadata
        
    Returns:
        dict with success status
    """
    try:
        # Ensure table exists before saving
        create_table_if_not_exists()
        
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        
        # Add timestamp
        metadata['file_id'] = file_id
        metadata['created_at'] = datetime.now().isoformat()
        
        table.put_item(Item=metadata)
        
        return {"success": True}
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to save metadata: {str(e)}"
        }


def get_metadata(file_id: str) -> dict:
    """
    Retrieve file metadata from DynamoDB.
    
    Args:
        file_id: Unique file identifier
        
    Returns:
        dict with metadata or error
    """
    try:
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        
        response = table.get_item(Key={'file_id': file_id})
        
        if 'Item' in response:
            return {
                "success": True,
                "metadata": response['Item']
            }
        else:
            return {
                "success": False,
                "error": "File not found"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve metadata: {str(e)}"
        }


def list_all_files(limit: int = 100) -> dict:
    """
    List all files from DynamoDB.
    
    Args:
        limit: Maximum number of items to return
        
    Returns:
        dict with list of files
    """
    try:
        # Ensure table exists
        create_table_if_not_exists()
        
        table = dynamodb.Table(DYNAMODB_TABLE_NAME)
        
        response = table.scan(Limit=limit)
        
        return {
            "success": True,
            "files": response.get('Items', []),
            "count": len(response.get('Items', []))
        }
        
    except Exception as e:
        print(f"DynamoDB list error: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to list files: {str(e)}",
            "files": [],
            "count": 0
        }


def test_dynamodb_connection() -> bool:
    """
    Test DynamoDB connection.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        create_table_if_not_exists()
        return True
    except Exception as e:
        print(f"❌ DynamoDB connection failed: {str(e)}")
        return False
