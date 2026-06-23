import anthropic
import PyPDF2
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def summarize_with_ai(text):
    return "AI generated summary here..."

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are an HR assistant. 
                Summarize the following document in a clear, 
                professional way. Extract key points like:
                - Main purpose of document
                - Key terms or conditions
                - Important dates or deadlines
                - Any action items
                
                Document:
                {text[:4000]}
                """
            }
        ]
    )
    return message.content[0].text