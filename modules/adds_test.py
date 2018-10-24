from grabbers import AddustourGrabber
import threading

import time

with open('./pdfs/downloadrecords.data', 'r+') as f: 
	download_recrods = f.read().splitlines()
	print(len(download_recrods))

grabber = AddustourGrabber('./addst_pdfs/pdf_urls.data',
 './adds_tpdfs/downloads/',
  './addst_pdfs/downloaded_urls.data',
  './addst_pdfs/records.data')
# pdf_urls = target(grabber.grab_pdfs)(from_=145877, to_=318935)

s = time.time()

start_2017 = 169280
start_2018 = 295901
end_2018 = 324524
lock = threading.Lock()
t1 = threading.Thread(target=grabber.grab_pdfs, args=[lock, start_2018,  303000])
t2 = threading.Thread(target=grabber.grab_pdfs, args=[lock, 303000, 311000])
t3 = threading.Thread(target=grabber.grab_pdfs, args=[lock, 311000, 319000])
t4 = threading.Thread(target=grabber.grab_pdfs, args=[lock, 319000, end_2018])

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()
print('time consumed', time.time()-s)
