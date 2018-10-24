from grabbers import AddustourGrabber
import threading
import time

grabber = AddustourGrabber('./addst_pdfs/pdf_urls.data',
 './adds_pdfs/downloads/',
  './addst_pdfs/downloaded_urls.data',
  './addst_pdfs/records.data')
s = time.time()

def download_pdfs(lock):
	for i in range(700):
		s2 = time.time()
		grabber.download_next(lock)
		print('time consumed', time.time()-s2)


lock = threading.Lock()
t1 = threading.Thread(target=download_pdfs, args=[lock])
# t2 = threading.Thread(target=download_pdfs, args=[lock])
# t3 = threading.Thread(target=download_pdfs, args=[lock])
# t4 = threading.Thread(target=download_pdfs, args=[lock])

t1.start()
# t2.start()
# t3.start()
# t4.start()

t1.join()
# t2.join()
# t3.join()
# t4.join()


