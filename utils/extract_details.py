import re

def extract_details(text, document_type):

    details = {
        "Name": None,
        "DOB": None,
        "Gender": None,
        "ID Number": None,
        "Address": None
    }

    lines = text.split("\n")

    # Clean OCR lines
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    # =====================================================
    # NAME EXTRACTION
    # =====================================================

    # ---------------- PAN CARD ----------------
    if document_type == "PAN Card":

        for i, line in enumerate(cleaned_lines):

            line_upper = line.upper()

            if "NAME" in line_upper:

                parts = line.split(":")

                if "NAME" in line_upper and "FATHER" not in line_upper:

                    # Case 1: Name is on the same line after colon
                    parts = line.split(":")

                    if len(parts) > 1 and parts[1].strip():
                        details["Name"] = parts[1].strip()
                        break
                    

                # Case 2: Name is on the next line
                    elif i + 1 < len(cleaned_lines):
                        next_line = cleaned_lines[i + 1]

                     # Skip noisy lines
                        if "FATHER" not in next_line.upper():
                            details["Name"] = next_line.strip()
                            break
                    
        

    # ---------------- AADHAAR CARD ----------------
    elif document_type == "Aadhaar Card":

        for line in cleaned_lines:

            line_upper = line.upper()

            # Skip noisy lines
            if (
                "GOVERNMENT" in line_upper
                or "INDIA" in line_upper
                or "DOB" in line_upper
                or "MALE" in line_upper
                or "FEMALE" in line_upper
                or "AUTHORITY" in line_upper
                or re.search(r"\d{4}\s?\d{4}\s?\d{4}", line)
            ):
                continue

            # probable name
            if len(line.split()) >= 2 and len(line) > 3:
                details["Name"] = line
                break

    # ---------------- PASSPORT ----------------
    elif document_type == "Passport":

        for line in cleaned_lines:

            line_upper = line.upper()

            # Skip noisy lines
            if (
                "REPUBLIC" in line_upper
                or "INDIA" in line_upper
                or "PASSPORT" in line_upper
                or "NATIONALITY" in line_upper
                or "PLACE OF ISSUE" in line_upper
                or re.search(r"[A-Z][0-9]{7}", line_upper)
            ):
                continue

            # Skip machine-readable code
            if "<" in line:
                continue

            # probable name
            if len(line.split()) >= 1 and len(line) > 3:
                details["Name"] = line
                break

    # ---------------- FALLBACK ----------------
    if details["Name"] is None:

        for line in cleaned_lines:

            line_upper = line.upper()

            if (
                len(line) > 3
                and "INDIA" not in line_upper
                and "DEPARTMENT" not in line_upper
                and "GOVT" not in line_upper
                and "REPUBLIC" not in line_upper
                and "AUTHORITY" not in line_upper
            ):

                if not re.search(r"\d", line):
                    details["Name"] = line
                    break

    # =====================================================
    # DOB EXTRACTION
    # =====================================================

    for i, line in enumerate(cleaned_lines):

        line_upper = line.upper()

        # Look for DOB keywords
        if (
            "DOB" in line_upper
            or "BIRTH" in line_upper
            or "DATE OF BIRTH" in line_upper
        ):

            dob_match = re.search(
                r"\d{2}/\d{2}/\d{4}",
                line
            )

            if dob_match:
                details["DOB"] = dob_match.group()
                break

            # Search next line
            if i + 1 < len(cleaned_lines):

                next_line = cleaned_lines[i + 1]

                dob_match = re.search(
                    r"\d{2}/\d{2}/\d{4}",
                    next_line
                )

                if dob_match:
                    details["DOB"] = dob_match.group()
                    break

    # ---------------- FALLBACK DOB ----------------
    if details["DOB"] is None:

        all_dates = re.findall(
            r"\d{2}/\d{2}/\d{4}",
            text
        )

        # Prefer older realistic DOBs
        for date in all_dates:

            year = int(date[-4:])

            if year < 2010:
                details["DOB"] = date
                break

    # =====================================================
    # GENDER EXTRACTION
    # =====================================================

    text_upper = text.upper()

    if "FEMALE" in text_upper:
        details["Gender"] = "Female"

    elif "MALE" in text_upper:
        details["Gender"] = "Male"

    # =====================================================
    # ADDRESS EXTRACTION
    # =====================================================

    address_lines = []

    capture = False

    stop_keywords = [
        "PRINT DATE",
        "UIDAI",
        "WWW",
        "GOV.IN",
        "HELP",
        "VID",
        "DOB",
        "YEAR OF BIRTH",
        "INCOME TAX",
        "GOVT",
        "PASSPORT"
    ]

    for line in cleaned_lines:

        line_upper = line.upper()

        # Start capture
        if (
            "ADDRESS" in line_upper
            or "ADDR" in line_upper
            or "C/O" in line_upper
        ):
            capture = True

        if capture:

            # Stop conditions
            if any(keyword in line_upper for keyword in stop_keywords):
                break

            # Stop Aadhaar number
            if re.search(r"\d{4}\s?\d{4}\s?\d{4}", line):
                break

            # Stop passport machine code
            if "<" in line:
                break

            # Ignore tiny noisy lines
            if len(line.strip()) < 3:
                continue

            address_lines.append(line)

    if address_lines:
        details["Address"] = " ".join(address_lines)

    return details








# # PaddleOCR
# import re

# def extract_details(text, document_type):

#     details = {
#         "Name": None,
#         "DOB": None,
#         "Gender": None,
#         "ID Number": None,
#         "Address": None
#     }

#     lines = [line.strip() for line in text.split("\n") if line.strip()]

#     # =========================
#     # PAN CARD
#     # =========================
#     if document_type == "PAN Card":

#         # PAN Number
#         pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"

#         pan_match = re.search(pan_pattern, text)

#         if pan_match:
#             details["ID Number"] = pan_match.group()

#         # DOB
#         dob_pattern = r"\d{2}/\d{2}/\d{4}"

#         dob_match = re.search(dob_pattern, text)

#         if dob_match:
#             details["DOB"] = dob_match.group()

#         # Name Extraction
#         for i, line in enumerate(lines):

#             if "NAME" in line.upper():

#                 if i + 1 < len(lines):
#                     details["Name"] = lines[i + 1]

#         # PAN usually has no address/gender
#         details["Gender"] = "Not Available"
#         details["Address"] = "Not Available"

#     # =========================
#     # AADHAAR CARD
#     # =========================
#     elif document_type == "Aadhaar Card":

#         # Aadhaar Number
#         aadhaar_pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"

#         aadhaar_match = re.search(aadhaar_pattern, text)

#         if aadhaar_match:
#             details["ID Number"] = aadhaar_match.group()

#         # DOB
#         dob_pattern = r"\d{2}/\d{2}/\d{4}"

#         dob_match = re.search(dob_pattern, text)

#         if dob_match:
#             details["DOB"] = dob_match.group()

#         # Gender
#         if "MALE" in text.upper():
#             details["Gender"] = "Male"

#         elif "FEMALE" in text.upper():
#             details["Gender"] = "Female"

#         # Name Extraction
#         for i, line in enumerate(lines):

#             if "GOVERNMENT OF INDIA" in line.upper():

#                 if i + 1 < len(lines):
#                     details["Name"] = lines[i + 1]

#         # Address Extraction
#         address_lines = []

#         capture = False

#         for line in lines:

#             if "ADDRESS" in line.upper():
#                 capture = True
#                 continue

#             if capture:

#                 if len(line) < 3:
#                     break

#                 address_lines.append(line)

#         details["Address"] = " ".join(address_lines)

#     return details