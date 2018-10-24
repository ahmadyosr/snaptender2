from grabbers import AlraiGrabber
import threading
import sys
import time


# with open('./alraipdfs/downloaded_urls.data', 'r+') as f: 
# 	download_recrods = f.read().splitlines()
# 	print(len(download_recrods))

grabber = AlraiGrabber('./alraipdfs/pdf_urls.data', './alraipdfs/downloads/', './alraipdfs/downloaded_urls.data')

grabber.grab_pdfs('10/10/2017','30/10/2017')

for i in range(10):
	f = grabber.download_next()
	print(f.url)
	print('downloaded')
# pdf_urls = target(grabber.grab_pdfs)(from_=145877, to_=318935)

# s = time.time()

# start = 145877
 
# t1 = threading.Thread(target=grabber.grab_pdfs, args=[start, 160000])
# t2 = threading.Thread(target=grabber.grab_pdfs, args=[160000, 175000])
# t3 = threading.Thread(target=grabber.grab_pdfs, args=[175000, 190000])
# t4 = threading.Thread(target=grabber.grab_pdfs, args=[205000, 220000])

# t1.start()
# t2.start()
# t3.start()
# t4.start()

# t1.join()
# t2.join()
# t3.join()
# t4.join()
# print('time consumed', time.time()-s)
