from pdf2image import convert_from_path
x= '/home/ahmad/dev/virtualenvs/tprocessing/tenders_modules/pdfs/downloads/file_317005'
def split(pdf_path, output_path):
	result = convert_from_path(x, output_folder='./')
	return print (result)

