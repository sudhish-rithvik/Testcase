"""Test script to check DynamoDB data"""
import sys
sys.path.append('.')

from app.services.dynamodb_service import list_all_files, get_metadata

# Open output file
output_file = open('db_test_output.txt', 'w', encoding='utf-8')

def log(msg):
    print(msg)
    output_file.write(msg + '\n')

# List all files
log("=" * 80)
log("LISTING ALL FILES IN DYNAMODB")
log("=" * 80)
result = list_all_files(10)

if result["success"]:
    log(f"\nFound {result['count']} files:\n")
    for i, file in enumerate(result["files"], 1):
        log(f"{i}. File ID: {file.get('file_id', 'N/A')}")
        log(f"   Filename: {file.get('filename', 'N/A')}")
        log(f"   Status: {file.get('status', 'N/A')}")
        log(f"   Has test_cases field: {'test_cases' in file}")
        if 'test_cases' in file:
            test_cases = file.get('test_cases', '')
            log(f"   Test cases length: {len(test_cases)} characters")
            if test_cases:
                log(f"   Test cases preview (first 200 chars): {test_cases[:200]}")
            else:
                log(f"   Test cases is EMPTY!")
        log("")
    
    # Get detailed info for first file
    if result["files"]:
        first_file_id = result["files"][0].get('file_id')
        log("=" * 80)
        log(f"DETAILED INFO FOR FIRST FILE: {first_file_id}")
        log("=" * 80)
        detailed_result = get_metadata(first_file_id)
        if detailed_result["success"]:
            metadata = detailed_result["metadata"]
            log(f"\nAll metadata keys: {list(metadata.keys())}")
            log(f"\nMetadata:")
            for key, value in metadata.items():
                if key == 'test_cases':
                    log(f"  {key}: {len(str(value))} characters")
                    if value:
                        log(f"    Preview: {str(value)[:300]}...")
                else:
                    log(f"  {key}: {value}")
else:
    log(f"Error: {result.get('error')}")

output_file.close()
log("\n\nOutput saved to db_test_output.txt")
