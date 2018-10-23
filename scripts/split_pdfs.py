from catalogue.models import Newspaper, NewspaperPage
from django.conf import settings 
import os 
import time 
from pdf2image import convert_from_path

def split_to_papers(paper):

	output_path = os.path.join(settings.MEDIA_ROOT, 'pages/'+paper.file.name)
	paper_path = os.path.join(settings.NEWSPAPERS_POOL_PATH, paper.file.name)
	
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	result = convert_from_path(paper_path, output_folder=output_path, thread_count=4, fmt='jpg')
	
	files = []
	for i,f in enumerate(result): 
		files += [NewspaperPage(page_no=i, newspaper=paper, image=f.filename)]
		
	NewspaperPage.objects.bulk_create(files)

	return result



newspapers = Newspaper.objects.filter(is_splitted=False)
done = []

for paper in newspapers : 
	print(paper.id)
	s = time.time()
	
	try : 
		split_to_papers(paper)
		paper.is_splitted = True
		paper.save() 
		done += [paper]
	except : 
		print('problem occured')

	print('time elapsed : ', time.time()-s)
