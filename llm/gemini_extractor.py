from google import genai
from PIL import Image
import json

# Initialize Client
client = genai.Client(api_key="API your key")


def extract_document_details(image_file):

    image = Image.open(image_file)

    prompt = """
    Analyze this identity document image.

    Classify the document type from:
    - Aadhaar Card
    - PAN Card
    - Voter ID
    - Passport
    - Driving License

    Extract:
    - Document Type
    - Name
    - DOB
    - Gender
    - ID Number
    - Address
    - Valid Till

    Return ONLY valid JSON.

    Example:
    {
        "Document Type": "PAN Card",
        "Name": "John Doe",
        "DOB": "01/01/1990",
        "Gender": "Male",
        "ID Number": "ABCDE1234F",
        "Address": "123 Main Street",
        "Valid Till": "01/01/2030"
    }
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image]
    )

    # Clean Gemini response
    cleaned_response = response.text.strip()

    cleaned_response = cleaned_response.replace("```json", "")
    cleaned_response = cleaned_response.replace("```", "")

    # Convert JSON string to Python dictionary
    result = json.loads(cleaned_response)

    return result
