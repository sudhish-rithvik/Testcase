import os
import time
import requests
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig, GoogleSearch

load_dotenv()

# Initialize Gemini client
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# Retry configuration
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 2  # seconds
TIMEOUT = 120  # seconds


def generate_testcases_with_retry(pdf_content: str):
    """
    Generate test cases with exponential backoff retry logic.
    """
    for attempt in range(MAX_RETRIES):
        try:
            return generate_healthcare_testcases(pdf_content)
        except Exception as e:
            error_str = str(e)
            
            # Handle different error types
            if "429" in error_str or "Resource has been exhausted" in error_str:
                # Rate limit error
                if attempt < MAX_RETRIES - 1:
                    delay = INITIAL_RETRY_DELAY * (2 ** attempt)
                    print(f"Rate limit hit. Retrying in {delay} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(delay)
                    continue
                else:
                    raise Exception("Rate limit exceeded after all retries")
            
            elif "timeout" in error_str.lower() or "Timeout" in error_str:
                # Timeout error
                if attempt < MAX_RETRIES - 1:
                    delay = INITIAL_RETRY_DELAY * (2 ** attempt)
                    print(f"Request timeout. Retrying in {delay} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(delay)
                    continue
                else:
                    raise Exception("Request timed out after all retries")
            
            elif "SSLEOFError" in error_str or "SSL" in error_str:
                # SSL/Connection error
                if attempt < MAX_RETRIES - 1:
                    delay = INITIAL_RETRY_DELAY * (2 ** attempt)
                    print(f"SSL error. Retrying in {delay} seconds... (Attempt {attempt + 1}/{MAX_RETRIES})")
                    time.sleep(delay)
                    continue
                else:
                    raise Exception("SSL connection failed after all retries")
            
            else:
                # Unknown error - raise immediately
                raise e
    
    raise Exception("Failed after all retry attempts")


def generate_healthcare_testcases(pdf_content: str):
    """
    Generate comprehensive healthcare test cases from PDF content using Gemini AI.
    
    Args:
        pdf_content: Extracted text content from PDF
        
    Returns:
        dict with generated test cases and solutions
    """
    # Enhanced prompt focused on clinical guidelines and CDSS testing
    prompt = f"""You are an expert QA engineer specializing in Clinical Decision Support Systems (CDSS) and medical software testing.

CLINICAL GUIDELINE/PROTOCOL DOCUMENT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pdf_content[:20000]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONTEXT:
This document contains clinical guidelines, treatment protocols, diagnostic pathways, hospital SOPs, or care guidelines that define decision logic for Clinical Decision Support Systems. These guidelines contain:
- Decision paths and branching logic
- Clinical thresholds and boundaries
- Exception handling rules
- Escalation protocols
- Multi-condition scenarios (symptoms + age + vitals)

YOUR MISSION:
Generate **8-10 focused, high-value test cases** that validate the decision logic and rule-based behavior described in this clinical guideline. Focus on:

1. **Decision Path Testing**: Test different clinical decision branches
2. **Threshold Validation**: Test boundary conditions and clinical thresholds
3. **Multi-Condition Scenarios**: Test combined conditions (e.g., symptom + age + vitals)
4. **Incomplete Data Handling**: Test missing or partial patient data
5. **Conflicting Rules**: Test scenarios where guidelines may conflict
6. **Edge Cases**: Test unusual but valid clinical situations

STRICT REQUIREMENTS:
- Generate **ONLY 8-10 test cases total** (not more!)
- Focus on **decision logic and rule validation**
- Include **specific clinical values** (vital signs, lab results, ages, etc.)
- Cover **both normal and edge cases**
- Prioritize **safety-critical scenarios**

OUTPUT FORMAT:

# Test Suite: [Clinical Guideline Name]

## Overview
**Guideline Type**: [Treatment Protocol / Diagnostic Pathway / ICU Protocol / Emergency Care]
**Criticality**: Critical
**Focus**: CDSS Decision Logic Validation

---

## Test Cases

### TC-001: [Decision Path Title]
**Priority**: P0-Critical
**Type**: Decision Path Validation

**Scenario**: [Describe the clinical scenario]

**Input Conditions**:
- Patient Age: [value]
- Vital Signs: [BP, HR, Temp, O2 Sat, etc.]
- Symptoms: [list]
- Lab Results: [if applicable]
- Medical History: [relevant details]

**Expected Decision/Action**:
- System should: [expected behavior]
- Alert/Recommendation: [what the CDSS should recommend]
- Rationale: [why this decision based on guideline]

**Validation Points**:
- ✓ Decision logic follows guideline Section X.Y
- ✓ All conditions properly evaluated (AND/OR logic)
- ✓ Recommendation matches protocol
- ✓ Escalation triggered if needed

---

### TC-002: [Boundary Condition Title]
**Priority**: P0-Critical
**Type**: Threshold Validation

**Scenario**: [Test a clinical threshold boundary]

**Input Conditions**:
- [Specific values at or near thresholds]
- Example: BP = 140/90 (exactly at hypertension threshold)

**Expected Decision/Action**:
- [What should happen at this exact threshold]

**Edge Cases to Test**:
- Value just below threshold: [expected result]
- Value at threshold: [expected result]
- Value just above threshold: [expected result]

---

### TC-003: [Multi-Condition Scenario]
**Priority**: P1-High
**Type**: Combined Conditions

**Scenario**: [Test multiple conditions together]

**Input Conditions**:
- Condition 1: [e.g., Age > 65]
- Condition 2: [e.g., Fever > 38.5°C]
- Condition 3: [e.g., Low O2 Sat < 92%]

**Expected Decision/Action**:
- [How system should handle multiple conditions]
- Priority: [which condition takes precedence]

---

### TC-004: [Incomplete Data Handling]
**Priority**: P1-High
**Type**: Missing Data

**Scenario**: [Test guideline with missing patient data]

**Input Conditions**:
- Available Data: [list]
- Missing Data: [critical missing fields]

**Expected System Behavior**:
- Should request: [missing data fields]
- Should/Should Not proceed: [Yes/No]
- Fallback protocol: [if any]

---

### TC-005: [Conflicting Guidelines]
**Priority**: P1-High  
**Type**: Rule Conflict

**Scenario**: [Test conflicting clinical rules]

**Input Conditions**:
- [Conditions that might trigger conflicting rules]

**Expected Decision/Action**:
- Resolution: [how conflict should be resolved]
- Priority: [which guideline takes precedence]

---

Continue with TC-006 through TC-010 following this pattern, covering:
- Normal/Happy path scenarios
- Different age groups (pediatric vs adult vs geriatric)
- Different severity levels
- Emergency vs non-emergency pathways
- Medication contraindications (if applicable)

## Implementation Notes

**Key Decision Points from Guideline**:
1. [List main decision points]
2. [List thresholds]
3. [List escalation criteria]

**Test Data Requirements**:
- Patient demographics (various ages, genders)
- Vital sign ranges (normal, borderline, critical)
- Lab value ranges
- Symptom combinations

**Compliance Checks**:
- HIPAA: Ensure test data is de-identified
- Clinical Accuracy: Validate against actual guideline
- Safety: Test all safety-critical decision paths

---

**REMEMBER**: Generate exactly **8-10 concise, focused test cases** that validate the clinical decision logic. Quality over quantity!

"""
    
    try:
        # Call Gemini API
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction="You are an expert healthcare software QA engineer specializing in Clinical Decision Support Systems testing.",
                temperature=0.7,
                top_p=0.95,
                max_output_tokens=8000,
                response_modalities=["TEXT"],
            )
        )
        
        # Extract the generated test cases
        test_cases_text = response.text if hasattr(response, 'text') else ""
        
        # Get usage metadata if available
        usage = {}
        if hasattr(response, 'usage_metadata'):
            usage = {
                "prompt_tokens": getattr(response.usage_metadata, 'prompt_token_count', 0),
                "completion_tokens": getattr(response.usage_metadata, 'candidates_token_count', 0),
                "total_tokens": getattr(response.usage_metadata, 'total_token_count', 0)
            }
        
        return {
            "text": test_cases_text,
            "model": MODEL_NAME,
            "usage": usage,
            "status": "success"
        }
        
    except Exception as e:
        error_msg = f"Test case generation failed: {str(e)}"
        print(f"Gemini API error: {error_msg}")
        return {
            "text": f"Error: {error_msg}",
            "model": MODEL_NAME,
            "usage": {},
            "status": "error",
            "error": error_msg
        }
