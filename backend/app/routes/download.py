from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, JSONResponse
from app.services.s3_service import get_file_from_s3, list_files_from_s3
from app.services.dynamodb_service import get_metadata, list_all_files

router = APIRouter()


@router.get("/download/testcases/{file_id}")
async def download_testcases_json(file_id: str):
    """
    Download test cases as JSON file.
    
    Args:
        file_id: Unique file identifier
        
    Returns:
        JSON file download
    """
    try:
        # Get metadata to find S3 key
        metadata_result = get_metadata(file_id)
        
        if not metadata_result["success"]:
            raise HTTPException(status_code=404, detail="File not found")
        
        testcases_url = metadata_result["metadata"].get("testcases_json_url")
        
        if not testcases_url:
            raise HTTPException(status_code=404, detail="Test cases not found for this file")
        
        # Extract S3 key from URL (s3://bucket/key)
        s3_key = testcases_url.replace(f"s3://{metadata_result['metadata'].get('filename', '')}/", "").split('/', 1)[1]
        
        # Download from S3
        file_result = get_file_from_s3(s3_key)
        
        if not file_result["success"]:
            raise HTTPException(status_code=500, detail=file_result.get("error"))
        
        return Response(
            content=file_result["content"],
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={file_id}-testcases.json"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.get("/download/markdown/{file_id}")
async def download_testcases_markdown(file_id: str):
    """
    Download test cases as Markdown file.
    
    Args:
        file_id: Unique file identifier
        
    Returns:
        Markdown file download
    """
    try:
        # Get metadata
        metadata_result = get_metadata(file_id)
        
        if not metadata_result["success"]:
            raise HTTPException(status_code=404, detail="File not found")
        
        testcases_url = metadata_result["metadata"].get("testcases_md_url")
        
        if not testcases_url:
            raise HTTPException(status_code=404, detail="Markdown test cases not found")
        
        # Extract S3 key
        s3_key = testcases_url.split('/', 3)[3]  # Get everything after bucket name
        
        # Download from S3
        file_result = get_file_from_s3(s3_key)
        
        if not file_result["success"]:
            raise HTTPException(status_code=500, detail=file_result.get("error"))
        
        return Response(
            content=file_result["content"],
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={file_id}-testcases.md"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.get("/download/pdf/{file_id}")
async def download_original_pdf(file_id: str):
    """
    Download original PDF file.
    
    Args:
        file_id: Unique file identifier
        
    Returns:
        PDF file download
    """
    try:
        # Get metadata
        metadata_result = get_metadata(file_id)
        
        if not metadata_result["success"]:
            raise HTTPException(status_code=404, detail="File not found")
        
        pdf_url = metadata_result["metadata"].get("pdf_s3_url")
        original_filename = metadata_result["metadata"].get("filename", "document.pdf")
        
        if not pdf_url:
            raise HTTPException(status_code=404, detail="PDF not found")
        
        # Extract S3 key
        s3_key = pdf_url.split('/', 3)[3]
        
        # Download from S3
        file_result = get_file_from_s3(s3_key)
        
        if not file_result["success"]:
            raise HTTPException(status_code=500, detail=file_result.get("error"))
        
        return Response(
            content=file_result["content"],
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={original_filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.get("/history")
async def get_upload_history(limit: int = 50):
    """
    Get history of all uploaded files.
    
    Args:
        limit: Maximum number of items to return (default: 50, max: 100)
        
    Returns:
        List of uploaded files with metadata
    """
    try:
        if limit > 100:
            limit = 100
        
        result = list_all_files(limit)
        
        if not result["success"]:
            # If table doesn't exist or other error, return empty list
            print(f"History error: {result.get('error')}")
            return {
                "count": 0,
                "files": []
            }
        
        return {
            "count": result["count"],
            "files": result["files"]
        }
        
    except Exception as e:
        print(f"History exception: {str(e)}")
        # Return empty list instead of error for better UX
        return {
            "count": 0,
            "files": []
        }



@router.get("/file/{file_id}")
async def get_file_info(file_id: str):
    """
    Get detailed information about a specific file.
    
    Args:
        file_id: Unique file identifier
        
    Returns:
        File metadata and S3 locations
    """
    try:
        result = get_metadata(file_id)
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail="File not found")
        
        return result["metadata"]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve file info: {str(e)}")
