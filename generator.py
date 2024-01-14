from latex import convert_latex_to_pdf
import time

class SRSGenerator:
  def __init__(self, data):
    self.name = data['name']
    self.description = data['description']
    self.style = data['style']

  def _create_prompt(self):
    return f'''Generate: SRS\nName: {self.name}\nDescription: {self.description}\nStyle: {self.style}\n'''
  

  def process(self, prompt):
    # hello world latex
    return f'''\\documentclass{{article}}
\\begin{{document}}
{prompt}
\\end{{document}}
'''
  
  
  def generate(self):
    # Generate a list of SRS cards  
    # need to implement this method
    prompt = self._create_prompt()

    latex = self.process(prompt)

    current_time_ms = str(int(time.time() * 1000))
    file_name = current_time_ms + '_' + self.name.replace(' ', '-').lower()

    convert_latex_to_pdf(latex, file_name)
    
    return {
      'file_url': f"http://127.0.0.1:5000/documents/{file_name}.pdf",
    }