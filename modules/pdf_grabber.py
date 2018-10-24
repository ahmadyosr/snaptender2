import requests
from abc import ABC, abstractmethod
import datetime 
import sys
import threading

"""
PDFs grabber for newspapers 
"""

class FileExists(Exception):
    pass

class File():
	def __init__(self, url, path, download_date):
		self.newspaper= ''  # ie : 'addustour'  
		self.url = url
		self.file_name = ''
		self.file_path = '' 
		self.newspaper_date = '' 
		self.download_date = '' 



class PapersGrabber(ABC):


	def __init__(self,records_file,  pdfs_directory, downloaded_file, log_file):
		self.pdfs_directory = pdfs_directory
		self.base_url = None
		self.records_file = records_file
		self.downloaded_file = downloaded_file
		self.log_file = log_file

		with open(records_file, 'r') as f : 
			self.pdf_urls = f.read().splitlines()

		with open(downloaded_file, 'r') as f2:
			self.downloaded_urls = f2.read().splitlines()

	@abstractmethod
	def grab_pdfs(self):
		pass

	def download_file(self, url):

		# r = requests.head(url)
		path = None 

		print('PDF Download ...')
		pdf_r = requests.get(url, stream=True)

		total_length  = pdf_r.headers.get('content-length')

		if total_length == None : 
			raise Exception('Has no Total length, its empty payload')
		else : 
			i = 1
			file_name  =  'file_' + url.split('=')[-1] # split :  'https://www.addustour.com/file.php?fileid=%d'
			path = './pdfs/downloads/' + file_name.split('/')[-1]
			
			with open(path , 'ab') as f :
				for l in pdf_r.iter_content(chunk_size=1024):
					f.write(l)
					i+= 1
		if path:
			return File(url, path, str(datetime.date.today()))
		
		return None 

	def download_next(self, lock):
		try : 
			url = self.pdf_urls.pop()
		except : 
			return
		file = self.download_file(url)
		sys.stdout.write(url +'/'+str(threading.currentThread().getName())+' ')

		lock.acquire()
		with open(self.records_file, 'w') as f : 
			for url_ in self.pdf_urls:
				f.write('%s\n' % url_)

		with open(self.downloaded_file, 'a') as df : 
			print('open downloaded')
			df.write('%s\n' % url)
		lock.release()
		return file
