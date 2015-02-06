# -*- coding: utf-8 -*-

import os, time, socket, datetime, SimpleHTTPServer, SocketServer, StringIO
import ImageGrab, subprocess

IMAGE_PATH = "C:\\Users\\Public\\tmp\\screen.png"
INTERVAL = 1
HTTP_DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"

def screenCapture(path):
  """Take screenshot if necessary"""
  try:
    # See if the current screenshot is stale
    t = os.stat(path)
    if((datetime.datetime.now() - datetime.datetime.fromtimestamp(t.st_mtime)) < datetime.timedelta(seconds=INTERVAL)):
      return
  except OSError:
    # File was not found
    pass
  img=ImageGrab.grab(bbox=(630,340,1290,775))
  img.save(IMAGE_PATH)

def formatPage():
  """Render HTML Page"""
  return """<html>
<head>
<title>Screen Sharing: %s</title>
<script language="JavaScript">
  counter = 0;
  function update() {
    document.getElementById("screenshot").src = "/screen.png?" + counter;
    self.setTimeout("update()",%s);
    counter++;
  }

  function launch() {
    document.getElementById("dummylaunch").src = "/launch";
  }

  function quit() {
    document.getElementById("dummyquit").src = "/quit";
  }
</script>
<style>
body { font-family: Lucida, Arial, "MS Trebuchet", sans-serif; }
.info { background-color: #DDD; padding: 4px; }
</style>
</head>
<body onload="update();">
<center>
<img id="screenshot" src="/screen.png">
<img id="dummylaunch" src="" style="display: none">
<img id="dummyquit" src="" style="display: none">
<br>
<button onclick="launch();">Launch a game</button>
<button onclick="quit();">Quit all games</button>
</center>
</body>
</html>""" % (socket.gethostname(), INTERVAL * 1000)

class LocalRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  """Custom HTTP Request Handler"""
  def send_head(self):
    """Common handler for GET and HEAD requests"""
    if self.path == "/":
      if False:
        subprocess.check_call(["C:\\Users\\Gab\'\\Downloads\\vampygarou\\Test\\V2\\VampiresVSWerewolves.exe"])
      self.send_response(200)
      self.send_header("Content-type","text/html")
      self.end_headers()
      return StringIO.StringIO(formatPage())

    if self.path[:11] == "/screen.png":
      try:
        screenCapture(IMAGE_PATH)
        f = open(IMAGE_PATH,'rb')
        self.send_response(200)
        self.send_header("Content-type","image/png")
        self.send_header("Content-Length", str(os.fstat(f.fileno()).st_size))
        mtime = datetime.datetime.fromtimestamp(os.fstat(f.fileno()).st_mtime)
        self.send_header("Last-Modified", mtime.strftime(HTTP_DATE_FORMAT))
        expires =  mtime + datetime.timedelta(seconds=INTERVAL)
        self.send_header("Expires", expires.strftime(HTTP_DATE_FORMAT))
        self.end_headers()
        return f
      except IOError:
        pass
    if self.path == "/launch":
      subprocess.Popen(["taskkill", "/im", "VampiresVSWerewolves.exe"])
      os.system('"cd C:\\Users\\Gab\'\\Downloads\\vampygarou\\Test\\V2\\ && START VampiresVSWerewolves.exe"')
      time.sleep(0.5)
      os.system('"cd C:\\Users\\Gab\'\\Downloads\\nircmd-x64\\ && nircmd.exe win center ititle \"Vampires\""')
      self.send_response(200)
      return None
    if self.path == "/quit":
      subprocess.Popen(["taskkill", "/im", "VampiresVSWerewolves.exe"])
      self.send_response(200)
      return None
    self.send_error(404, "File not found")
    return None

if __name__=='__main__':
  screenCapture(IMAGE_PATH)
  httpd = SocketServer.TCPServer(('',5550),LocalRequestHandler)
  httpd.serve_forever()
