import requests
import time
import random

# 1. Use a stable model with better rate limits
# gemini-2.5-flash is the newest stable model (June 2025) with excellent rate limits
MODEL_NAME = "gemini-2.5-flash"

# 2. Hardcode your NEW API Key here (ensure NO spaces inside the quotes)
API_KEY = "AIzaSyAWEYhyz5au9vV04QQ8GG7YMIXARxUPtss"  

def call_gemini(prompt: str):
    # Using v1beta as it supports the newest 2.x models shown in your list
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    max_retries = 3
    base_delay = 2  # seconds

    for attempt in range(max_retries + 1):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=120)

            if response.status_code == 429:
                if attempt < max_retries:
                    # Exponential backoff with jitter
                    wait_time = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                    print(f"Gemini API rate limit hit (429). Retrying in {wait_time:.2f} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    # Return distinct error if max retries hit
                    return {
                        "error": "Gemini API rate limit exceeded after multiple retries",
                        "status_code": 429,
                        "details": response.json() if response.content else response.text
                    }

            if response.status_code != 200:
                return {
                    "error": "Gemini API failed",
                    "status_code": response.status_code,
                    "details": response.json() if response.content else response.text
                }

            data = response.json()
            
            # Safe extraction of text
            if "candidates" in data and data["candidates"]:
                return {
                    "text": data["candidates"][0]["content"]["parts"][0]["text"],
                    "model": data.get("modelVersion"),
                    "usage": data.get("usageMetadata"),
                }
            else:
                return {"error": "No candidates returned", "raw_response": data}

        except requests.exceptions.Timeout:
            if attempt < max_retries:
                wait_time = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                print(f"Gemini API timeout. Retrying in {wait_time:.2f} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                return {"error": "Gemini API timeout after multiple retries"}
        except requests.exceptions.SSLError as ssl_err:
            if attempt < max_retries:
                wait_time = (base_delay * (2 ** attempt)) + random.uniform(0, 1)
                print(f"SSL connection error. Retrying in {wait_time:.2f} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                continue
            else:
                return {"error": f"SSL connection failed after multiple retries: {str(ssl_err)}"}
        except Exception as e:
            return {"error": f"Connection error: {str(e)}"}


def generate_healthcare_testcases(pdf_content: str):
    """
    Generate comprehensive healthcare test cases from PDF content using Gemini AI.
    
    Args:
        pdf_content: Extracted text content from PDF
        
    Returns:
        dict with generated test cases and solutions
    """
    # Enhanced prompt for superior healthcare test case generation
    prompt = f"""You are a senior healthcare software QA engineer with expertise in medical software testing, HIPAA compliance, and clinical workflows.

HEALTHCARE DOCUMENT TO ANALYZE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{pdf_content[:20000]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

YOUR MISSION:
Analyze this healthcare document and generate production-ready test cases following industry best practices for medical software testing.

OUTPUT STRUCTURE (Use this exact format):

# TEST SUITE: [Feature/Module Name]

## 📋 FEATURE OVERVIEW
- **Description**: [Brief description of the feature]
- **Healthcare Domain**: [e.g., EHR, Telemedicine, Lab Management, etc.]
- **Criticality**: [Critical/High/Medium/Low]
- **Compliance Requirements**: [HIPAA, HL7, FHIR, FDA, etc.]

---

## ✅ POSITIVE TEST CASES

### TC-[ID]: [Test Case Title]
**Priority**: [P0-Critical / P1-High / P2-Medium / P3-Low]  
**Category**: [Functional/Integration/UI/Performance]

**Preconditions**:
- [Condition 1]
- [Condition 2]

**Test Steps**:
1. [Detailed step 1]
2. [Detailed step 2]
3. [Continue...]

**Test Data**:
- [Specific test data with examples]
- Example: PatientID: "P123456", DOB: "01/01/1980"

**Expected Result**:
- [Clear, measurable expected outcome]

**Healthcare-Specific Validations**:
- [ ] Data privacy maintained (PHI not exposed)
- [ ] Audit trail created
- [ ] User permissions verified
- [ ] Clinical accuracy validated

---

## ❌ NEGATIVE TEST CASES

### TC-[ID]: [Test Case Title]
[Same structure as positive tests, focusing on error scenarios]

---

## 🔒 SECURITY TEST CASES

### TC-[ID]: [Test Case Title]
**Focus**: [Authentication/Authorization/Encryption/Audit/Data Privacy]

[Include specific healthcare security concerns:]
- HIPAA violation prevention
- PHI/PII protection
- Role-based access control
- Session management
- SQL injection prevention
- XSS prevention

---

## ⚡ EDGE CASES & BOUNDARY CONDITIONS

### TC-[ID]: [Test Case Title]
[Test unusual but valid scenarios:]
- Maximum field lengths
- Special characters in medical data
- Concurrent user access
- Network interruptions during critical operations
- Extremely large datasets

---

## 🏥 HEALTHCARE-SPECIFIC SCENARIOS

### TC-[ID]: Emergency Scenario - [Title]
**Critical Path**: Yes/No
**Response Time Requirement**: [e.g., < 2 seconds]

[Test emergency scenarios:]
- Code Blue situations
- Urgent medication orders
- Critical lab results
- Emergency patient registration

---

## 🔄 INTEGRATION TEST CASES

### TC-[ID]: [System Integration Title]
[Test integrations with:]
- HL7 message exchange
- FHIR API calls
- Medical device interfaces
- Pharmacy systems
- Insurance verification systems
- Lab information systems

---

## 💊 MEDICATION SAFETY TEST CASES

### TC-[ID]: [Medication Safety Title]
[Test critical medication workflows:]
- Drug-drug interactions
- Allergy checking
- Dosage calculation validation
- Duplicate medication prevention
- High-risk medication alerts

---

## 📊 DATA VALIDATION & ACCURACY

### TC-[ID]: [Data Validation Title]
[Test medical data accuracy:]
- Vital signs range validation
- ICD-10 code validation
- CPT code validation
- Laboratory result ranges
- Medical terminology standardization

---

## 🎯 RECOMMENDED SOLUTIONS & IMPLEMENTATION NOTES

**For Developers:**
1. [Specific implementation suggestion]
2. [Security best practice]
3. [Performance optimization tip]

**For QA Team:**
1. [Testing strategy recommendation]
2. [Automation opportunity]
3. [Risk mitigation approach]

**Compliance Checklist:**
- [ ] HIPAA Security Rule compliance verified
- [ ] HIPAA Privacy Rule compliance verified
- [ ] Minimum necessary principle applied
- [ ] Business Associate Agreement requirements met
- [ ] Breach notification procedures tested

---

## 🚨 CRITICAL ISSUES TO WATCH

1. [Potential security vulnerability]
2. [Data integrity concern]
3. [Compliance risk]

---

QUALITY REQUIREMENTS FOR YOUR OUTPUT:
✓ Each test case must be executable without ambiguity
✓ Include specific, realistic healthcare test data
✓ Cover ALL mentioned features in the document
✓ Prioritize test cases (P0/P1/P2/P3)
✓ Include traceability to requirements
✓ Provide both manual and automation guidance
✓ Consider multi-user and concurrent access scenarios
✓ Include performance benchmarks where applicable
✓ Add specific HIPAA compliance checkpoints
✓ Ensure clinical workflow integrity

Generate comprehensive test cases NOW."""

    return call_gemini(prompt)
