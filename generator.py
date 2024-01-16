import time


class SRSGenerator:
  def __init__(self, data):
    self.name = data['name']
    self.description = data['description']

  def _create_prompt(self):
    return f'''Generate: SRS\nName: {self.name}\nDescription: {self.description}\n'''
  

  def init_process(self, prompt):
    # TODO: create a sub_process which calls the python script that is responsible to generate SRS
    return ''

  def generate(self):
    # Generate a list of SRS cards  
    # need to implement this method
    prompt = self._create_prompt()

    latex = self.process(prompt)

    current_time_ms = str(int(time.time() * 1000))
    file_name = current_time_ms + '_' + self.name.replace(' ', '-').lower()

    # TODO: convert to pdf

    return {
      'file_url': f"http://127.0.0.1:5000/documents/{file_name}.pdf",
    }