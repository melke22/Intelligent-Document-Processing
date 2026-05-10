# import re

# def mask_sensitive_data(data):

#     # Mask Aadhaar
#     if "ID Number" in data and data["ID Number"]:

#         id_number = data["ID Number"]

#         # Aadhaar
#         if re.match(r"\d{4}\s?\d{4}\s?\d{4}", id_number):

#             data["ID Number"] = "XXXX XXXX " + id_number[-4:]

#         # PAN
#         elif re.match(r"[A-Z]{5}[0-9]{4}[A-Z]", id_number):

#             data["ID Number"] = id_number[:5] + "****" + id_number[-1]

#         # Passport
#         elif re.match(r"[A-Z]{2}[0-9]{6}", id_number):

#             data["ID Number"] = id_number[:3] + "*******" + id_number[-1]

#         # Voter ID
#         elif re.match(r"[A-Z]{3}[0-9]{7}", id_number):

#             data["ID Number"] = id_number[:3] + "*******" + id_number[-1]

#     return data



import re

def mask_sensitive_data(data):

    if "ID Number" in data:

        id_info = data["ID Number"]

        # Extract actual value
        id_number = id_info.get("value", "")

        # Aadhaar masking
        if re.match(r"\d{4}\s?\d{4}\s?\d{4}", id_number):

            masked = "XXXX XXXX " + id_number[-4:]

            data["ID Number"]["value"] = masked

        # PAN masking
        elif re.match(r"[A-Z]{5}[0-9]{4}[A-Z]", id_number):

            masked = id_number[:5] + "****" + id_number[-1]

            data["ID Number"]["value"] = masked

    return data