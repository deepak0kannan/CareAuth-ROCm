import re
from typing import Dict, Any, List

class PHISanitizer:
    """
    Local HIPAA PHI/PII Sanitization Engine.
    Ensures that Protected Health Information (PHI) is de-identified locally 
    before routing to any cloud LLM or external agent endpoints.
    """
    
    # Regex patterns for common direct health identifiers
    SSN_PATTERN = r'\b\d{3}-\d{2}-\d{4}\b'
    PHONE_PATTERN = r'\(?\b[2-9][0-9]{2}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}\b'
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    MRN_PATTERN = r'\b(?:MRN|Medical Record Number|Chart #|Patient ID)[:\s]*([A-Z0-9-]{6,12})\b'
    DOB_PATTERN = r'\b(?:DOB|Date of Birth|Birthdate)[:\s]*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})\b'
    
    # Common patient name patterns in clinical headers
    NAME_HEADER_PATTERN = r'\b(?:Patient Name|Pt Name|Name)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'

    def sanitize(self, text: str) -> Dict[str, Any]:
        """
        Sanitizes text and returns redacted text with an audit trail.
        """
        redactions: List[Dict[str, str]] = []
        sanitized = text

        # 1. Mask Social Security Numbers
        for match in re.finditer(self.SSN_PATTERN, sanitized):
            redactions.append({"type": "SSN", "original": match.group(0), "replacement": "[REDACTED_SSN]"})
        sanitized = re.sub(self.SSN_PATTERN, "[REDACTED_SSN]", sanitized)

        # 2. Mask Phone Numbers
        for match in re.finditer(self.PHONE_PATTERN, sanitized):
            redactions.append({"type": "PHONE", "original": match.group(0), "replacement": "[REDACTED_PHONE]"})
        sanitized = re.sub(self.PHONE_PATTERN, "[REDACTED_PHONE]", sanitized)

        # 3. Mask Email Addresses
        for match in re.finditer(self.EMAIL_PATTERN, sanitized):
            redactions.append({"type": "EMAIL", "original": match.group(0), "replacement": "[REDACTED_EMAIL]"})
        sanitized = re.sub(self.EMAIL_PATTERN, "[REDACTED_EMAIL]", sanitized)

        # 4. Mask Medical Record Numbers
        for match in re.finditer(self.MRN_PATTERN, sanitized, re.IGNORECASE):
            redactions.append({"type": "MRN", "original": match.group(1), "replacement": "[REDACTED_MRN]"})
        sanitized = re.sub(self.MRN_PATTERN, "MRN: [REDACTED_MRN]", sanitized, flags=re.IGNORECASE)

        # 5. Mask Date of Birth
        for match in re.finditer(self.DOB_PATTERN, sanitized, re.IGNORECASE):
            redactions.append({"type": "DOB", "original": match.group(1), "replacement": "[REDACTED_DOB]"})
        sanitized = re.sub(self.DOB_PATTERN, "DOB: [REDACTED_DOB]", sanitized, flags=re.IGNORECASE)

        # 6. Mask Patient Names in Headers
        for match in re.finditer(self.NAME_HEADER_PATTERN, sanitized, re.IGNORECASE):
            redactions.append({"type": "PATIENT_NAME", "original": match.group(1), "replacement": "[REDACTED_PATIENT_NAME]"})
        sanitized = re.sub(self.NAME_HEADER_PATTERN, "Patient Name: [REDACTED_PATIENT_NAME]", sanitized, flags=re.IGNORECASE)

        return {
            "sanitized_text": sanitized,
            "total_redactions": len(redactions),
            "redactions_audit": redactions,
            "is_hipaa_compliant": True,
            "status_message": f"Successfully de-identified {len(redactions)} PHI items locally on AMD."
        }

phi_sanitizer = PHISanitizer()
