class ApiException(Exception):
  def __init__(self, message, status_code):
    super().__init__(message)
    self.message = message
    self.status_code = status_code
    self.payload = {
      'message': self.message,
      'success': False
    }

  def to_dict(self):
    return self.payload