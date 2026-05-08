import re

def classify_document(text):

    text = text.upper()

    #aadhaar_pattern = r"\b\d{4}\s\d{4}\s\d{4}\b"
    aadhaar_pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"
    pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    voter_pattern = r"\b[A-Z]{3}[0-9]{7}\b"
    passport_pattern = r"[A-Z\$][0-9]{7}"

    if re.search(aadhaar_pattern, text):
        return "Aadhaar Card"

    elif re.search(pan_pattern, text):
        return "PAN Card"

    elif re.search(voter_pattern, text):
        return "Voter ID"

    elif re.search(passport_pattern, text):
        return "Passport"

    else:
        return "Unknown Document"

        




# #PaddleOCR based classification for better accuracy
# import re

# def classify_document(text):

#     text = text.upper()

#     aadhaar_pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"
#     pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"

#     if re.search(aadhaar_pattern, text):
#         return "Aadhaar Card", 95

#     elif re.search(pan_pattern, text):
#         return "PAN Card", 98

#     else:
#         return "Unknown Document", 50