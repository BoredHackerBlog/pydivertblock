import urllib.request
import time
import threading
import pydivert

listsite = "http://your.site/blocklist.txt"

blocklist = []

updateduration = 10

def updatelist(): #this downloads new blocklist from listsite and sleeps for updateduration before re-downloading
    global blocklist
    while True:
        request_content = urllib.request.urlopen(listsite).read()
        blocklist = request_content.decode("utf-8").splitlines()
        time.sleep(updateduration)

def block():
    global blocklist
    with pydivert.WinDivert("ip") as w: #check windivert filter language docs
        for packet in w:
            if packet.dst_addr in blocklist: #if dst ip in blocklist, pass
                pass
            else:
                w.send(packet) #send if dst ip not in blocklist

update_thread = threading.Thread(target=updatelist)
update_thread.daemon = True
update_thread.start()

block_thread = threading.Thread(target=block)
block_thread.daemon = True
block_thread.start()

block_thread.join()
