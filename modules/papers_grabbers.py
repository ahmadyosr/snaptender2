import requests
import sys
file_id = 323935

url = 'https://www.addustour.com/file.php?fileid=%d&view=1' % file_id
pdf_r = requests.get(url)
print(pdf_r.text)
# with open('x.pdf', 'wb') as f:
	# f.write(pdf.)
sys.exit('')

file_id = 323935
# get time of execution 
# write pdf id to file 

while file_id > 323434:
	print('---')
	file_id -= 1

	url = 'https://www.addustour.com/file.php?fileid=%d&view=1' % file_id
	r = requests.head(url)
	if r.headers['content-type'] == 'application/pdf' : 
		print('PDF FOUND , file_id: #')
		print(file_id)
		pdf_r = requests.get(url)
		print(pdf_r.text)
		total_length  = pdf_r.headers.get('content-length', stream=True)


		if total_length == None : 
			break
		else : 
			i = 1
			with open('download.file', 'ab') as f :
				for l in pdf_r.iter_content(chunk_size=512):
					f.write(l)
					print(i, end=' ')
					i+= 1
				print('# of lines ', i)


