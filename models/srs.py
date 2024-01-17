from db import get_db
from errors.ApiException import ApiException

class SrsModel:
  @staticmethod
  def save_to_db(data: dict):
    conn = get_db()
    try: 
      cursor = conn.execute('INSERT INTO srs (name, description,task_id) VALUES (?, ?, ?)', (data['name'], data['description'], data['task_id']))
      conn.commit() 

    except Exception as e:
      conn.rollback()
      raise ApiException('Error while saving to database', 500)
    return SrsModel.get_by_id(cursor.lastrowid)

  @staticmethod
  def convert_data(row):
    if row is None:
      return ApiException('SRS not found', 404)
    print(list(row))
    data = {
      'id': row[0],
      'task_id': row[1],
      'name': row[2],
      'description': row[3],
      'created': row[4],
      'is_completed': bool(row[5]),
      'file_url': row[6]
    }
    return data

  @staticmethod
  def get_by_id(id: int):
    conn = get_db()
    try:
      print(id)
      cursor = conn.execute('SELECT id, task_id, name, description, created, is_completed, file_url FROM srs WHERE id = ?', (id,))
      row = cursor.fetchone()
    except Exception as e:
      print(e)
      raise ApiException('Error while fetching from database', 500)
    return SrsModel.convert_data(row)
  
  @staticmethod
  def get_task_id(id: int):
    conn = get_db()
    try:
      print(id)
      cursor = conn.execute('SELECT task_id FROM srs WHERE id = ?', (id,))
      row = cursor.fetchone()
    except Exception as e:
      print(e)
      raise ApiException('Error while fetching from database', 500)
    return {'task_id': row[0]}