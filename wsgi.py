import eventlet
eventlet.monkey_patch()
import subprocess
from app import app, celery_app

if __name__ == "__main__":
  active_workers = celery_app.control.inspect().active() 

  if active_workers == None:
      cmd = "celery -A app.celery_app worker -Q specific_queue --pool=eventlet".split(' ')
      subprocess.Popen(cmd)

  app.run()
