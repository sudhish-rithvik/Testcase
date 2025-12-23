"""
Test script to verify AWS S3 and DynamoDB connectivity.
Run this to ensure your AWS credentials are working correctly.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.s3_service import test_s3_connection
from app.services.dynamodb_service import test_dynamodb_connection

def main():
    print("=" * 60)
    print("Testing AWS Connectivity")
    print("=" * 60)
    
    print("\n1. Testing S3 Connection...")
    s3_success = test_s3_connection()
    
    print("\n2. Testing DynamoDB Connection...")
    dynamodb_success = test_dynamodb_connection()
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"S3: {'✅ Connected' if s3_success else '❌ Failed'}")
    print(f"DynamoDB: {'✅ Connected' if dynamodb_success else '❌ Failed'}")
    
    if s3_success and dynamodb_success:
        print("\n🎉 All AWS services are connected successfully!")
        return 0
    else:
        print("\n⚠️ Some AWS services failed to connect. Check your credentials in .env file.")
        return 1

if __name__ == "__main__":
    exit(main())
