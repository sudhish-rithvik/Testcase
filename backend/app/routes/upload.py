from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import extract_text_from_pdf, validate_pdf_content
from app.services.gemini_service import generate_healthcare_testcases
from app.services.s3_service import upload_pdf_to_s3, upload_testcases_to_s3
from app.services.dynamodb_service import save_metadata

router = APIRouter()

# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, generate healthcare test cases, and store in AWS S3.
    
    Args:
        file: PDF file to upload
        
    Returns:
        JSON response with extracted text, generated test cases, and S3 locations
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed. Please upload a file with .pdf extension."
        )
    
    try:
        # Read file content
        pdf_bytes = await file.read()
        
        # Validate file size
        if len(pdf_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE // (1024 * 1024)}MB"
            )
        
        # Extract text from PDF
        extraction_result = extract_text_from_pdf(pdf_bytes)
        
        if not extraction_result["success"]:
            raise HTTPException(
                status_code=400,
                detail=extraction_result.get("error", "Failed to extract text from PDF")
            )
        
        extracted_text = extraction_result["text"]
        num_pages = extraction_result["pages"]
        
        # Validate content
        if not validate_pdf_content(extracted_text):
            raise HTTPException(
                status_code=400,
                detail="PDF does not contain sufficient text content. Minimum 50 characters required."
            )
        
        # Upload original PDF to S3
        s3_upload_result = upload_pdf_to_s3(pdf_bytes, file.filename)
        
        if not s3_upload_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload PDF to S3: {s3_upload_result.get('error')}"
            )
        
        file_id = s3_upload_result["file_id"]
        pdf_s3_url = s3_upload_result["s3_url"]
        
        # Generate healthcare test cases using Gemini AI
        test_cases_result = generate_healthcare_testcases(extracted_text)
        
        # Check for errors in AI generation
        if "error" in test_cases_result:
            # Still save metadata even if test case generation failed
            metadata = {
                "filename": file.filename,
                "pages": num_pages,
                "extracted_text_length": len(extracted_text),
                "pdf_s3_url": pdf_s3_url,
                "status": "partial_success",
                "error": test_cases_result["error"]
            }
            save_metadata(file_id, metadata)
            
            return {
                "file_id": file_id,
                "filename": file.filename,
                "pages": num_pages,
                "extracted_text_length": len(extracted_text),
                "s3_locations": {
                    "pdf_url": pdf_s3_url
                },
                "test_cases": None,
                "error": test_cases_result["error"],
                "status": "partial_success"
            }
        
        # Upload test cases to S3 (JSON format)
        testcases_json_result = upload_testcases_to_s3(
            test_cases_result,
            file.filename,
            file_id,
            format_type="json"
        )
        
        # Upload test cases to S3 (Markdown format)
        testcases_md_result = upload_testcases_to_s3(
            test_cases_result,
            file.filename,
            file_id,
            format_type="markdown"
        )
        
        # Save metadata to DynamoDB
        metadata = {
            "filename": file.filename,
            "pages": num_pages,
            "extracted_text_length": len(extracted_text),
            "pdf_s3_url": pdf_s3_url,
            "testcases_json_url": testcases_json_result.get("s3_url"),
            "testcases_md_url": testcases_md_result.get("s3_url"),
            "test_cases": test_cases_result.get("text", ""),  # Add test cases text
            "model_used": test_cases_result.get("model", "gemini-2.5-flash"),
            "token_usage": str(test_cases_result.get("usage", {})),
            "status": "success"
        }
        
        save_result = save_metadata(file_id, metadata)
        
        if not save_result["success"]:
            print(f"Warning: Failed to save metadata to DynamoDB: {save_result.get('error')}")
        
        # Return successful response
        return {
            "file_id": file_id,
            "filename": file.filename,
            "pages": num_pages,
            "extracted_text_length": len(extracted_text),
            "s3_locations": {
                "pdf_url": pdf_s3_url,
                "testcases_json_url": testcases_json_result.get("s3_url"),
                "testcases_md_url": testcases_md_result.get("s3_url")
            },
            "test_cases": test_cases_result,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
