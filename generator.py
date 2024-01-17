import torch
from transformers import pipeline
import os
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, PageTemplate
from reportlab.lib.pagesizes import letter
from models.srs import SrsModel
import datetime as dt
class SRSGenerator:
  def __init__(self):
    self.pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")
    
  
  def _create_prompt(self, name, description):
    return f'Generate an SRS document where the topic is {name} and description is {description}'
  
  
  def _infer(self, prompt):
    return self.pipe(prompt, max_new_tokens=1024, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
  
  
  def generate_srs(self,data,database ):
    prompt = self._create_prompt(data['name'],data['description'])
    messages = [
    {
        "role": "system",
        "content": "You are a chatbot who can generate an SRS document!",
    },
    {"role": "user", "content": f"{prompt}"},
]
    prompt = self.pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True) 
    print('Inference starting')
    outputs = self._infer(prompt)
    srs_output = outputs[0]["generated_text"].split('<|assistant|>\n')[1]
    file_url = self._create_pdf(data['name'], srs_output)
    # file_url = f"http://127.0.0.1:5000/documents/{file_name}.pdf"
    updated_data = { 'id':data['id'], "file_url":file_url, "is_completed":1}
    srs = SrsModel.update_in_db(updated_data)
    print("Database Updated")


  def _create_pdf(self, title, text):    
    file_name = dt.datetime.now(dt.timezone.utc).timestamp()

    if not os.path.exists('assets/documents'):
      os.makedirs('assets/documents')
    # Create pdf doc  
    pdf_path = f"assets/documents/{file_name}.pdf"

    # Define margins
    left_margin = 36
    right_margin = 36
    top_margin = 36
    bottom_margin = 36

    # Create a SimpleDocTemplate
    pdf_doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                                leftMargin=left_margin, rightMargin=right_margin,
                                topMargin=top_margin, bottomMargin=bottom_margin)

    # Define a frame with adjusted margins
    frame = Frame(left_margin, bottom_margin, letter[0] - left_margin - right_margin,
                  letter[1] - top_margin - bottom_margin, showBoundary=False)

    # Create a PageTemplate and add the frame to it
    page_template = PageTemplate(id='main', frames=[frame])

    # Add the PageTemplate to the SimpleDocTemplate
    pdf_doc.addPageTemplates([page_template])

    # Set font to Times New Roman
    styles = getSampleStyleSheet()

    # Title
    title_paragraph = Paragraph(title, styles['Title'])
    text_paragraphs = [Paragraph(line, styles['BodyText']) for line in text.split('\n')]

    # Build a Story with paragraphs
    story = [title_paragraph] + text_paragraphs
    
    # Build the PDF document with the Story
    pdf_doc.build(story)
    return f"assets/documents/{file_name}.pdf"
