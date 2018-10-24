import requests
from pdf_grabber import PapersGrabber
import sys
import datetime
import threading
class AddustourGrabber(PapersGrabber):

	def __init__(self,records_file,  pdfs_directory, local_files_urls, log_file):
		super().__init__(records_file, pdfs_directory, local_files_urls, log_file)	
		self.base_url =  'https://www.addustour.com/file.php?fileid=%d'

	def grab_pdfs(self,lock,  from_, to_):

		resource_id = from_

		finds_urls = []
		while(resource_id <= to_ ):
			sys.stdout.write(str(to_-resource_id)+'/'+str(threading.currentThread().getName())+' ')
			sys.stdout.flush()
			resource_id += 1
	
			count_404 = 0 
			resource_url = self.base_url % resource_id

			lock.acquire()
			with open(self.log_file, 'a') as f :
				f.write('%s\n'%resource_url)
			lock.release()

			r = requests.head(resource_url)

			if r.status_code != 200 : 
				count_404 += 1
				continue
			if r.headers['content-type'] == 'application/pdf' : 
				print('PDF Found')
				finds_urls += [resource_url]

				if (resource_url not in self.pdf_urls) and (resource_url not in self.downloaded_urls): 
					lock.acquire()
					with open(self.records_file, 'a') as pf:
						pf.write('%s\n' % resource_url)
					lock.release()	
			
		return finds_urls


class AlraiGrabber(PapersGrabber):

	def __init__(self,records_file,  pdfs_directory, local_files_urls):
		super().__init__(records_file, pdfs_directory, local_files_urls)	
		self.base_url =  'http://alrai.com/uploads/pdf/%Y/%m/%d/alrai-%Y%m%df.pdf'
		
	def grab_pdfs(self, from_ , to_):
		from_date = datetime.datetime.strptime(from_, '%d/%m/%Y').date()
		to_date = datetime.datetime.strptime(to_, '%d/%m/%Y').date()

		while(from_date <= to_date):

			url = from_date.strftime(self.base_url)
			print(url)
			r = requests.head(url)		
			from_date += datetime.timedelta(days=1)		

			print(r.headers['content-type'])

			if r.headers['content-type'] == 'application/pdf' : 
				if (url not in self.pdf_urls) and (url not in self.downloaded_urls): 
					with open(self.records_file, 'a') as pf:
						pf.write('%s\n' % url)
			
