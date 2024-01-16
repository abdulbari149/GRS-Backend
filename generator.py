import torch
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor
import os
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, PageTemplate
from reportlab.lib.pagesizes import letter
from db import get_db
from models.srs import SrsModel
import datetime


class SRSGenerator:
  
  def __init__(self):
    self.pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", torch_dtype=torch.bfloat16, device_map="auto")
    self.executor = ThreadPoolExecutor()
  
  def _create_prompt(self,name,description):
    return f'Generate an SRS document where the topic is {name} and description is {self.description}'
  
  
  def _infer(self, prompt):
    return self.pipe(prompt, max_new_tokens=1024, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
  
  
  def _generate_srs(self,name,description, file_name):
    prompt = self._create_prompt(name,description)
    messages = [
    {
        "role": "system",
        "content": "You are a chatbot who can generate an SRS document!",
    },
    {"role": "user", "content": f"{prompt}"},
]
    prompt = self.pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True) 
    outputs = self._infer(prompt)
    
    srs_output = outputs[0]["generated_text"].split('<|assistant|>\n')[1]
    pdf_path = self._create_pdf(name, srs_output, file_name)
    file_url = f"http://127.0.0.1:5000/documents/{file_name}.pdf"
    db = get_db()
    srs = SrsModel(name=name, description=description, file_url=file_url, is_completed=1)
    db.session.add(srs)
    db.session.commit()


  def _create_pdf(self, title, text, file_name):    
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
    
def generate_and_save_srs_async(self, name, description):
        file_name = datetime.now(datetime.timezone.utc).timestamp()
        self.executor.submit(self._generate_srs, name, description, file_name)

def get_srs_status(self, srs_id):
        db = get_db()
        srs = SrsModel.query.get(srs_id)
        if srs:
            return {
                'id': srs.id,
                'name': srs.name,
                'description': srs.description,
                'file_url': srs.file_url,
                'is_completed': srs.is_completed
            }
        else:
            return None
    
    
      
      
        