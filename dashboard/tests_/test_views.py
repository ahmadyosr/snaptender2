from django.test import TestCase
from catalogue.tests_.test_models import NewspaperTestCase, TenderTestCase
from shutil import copyfile
from catalogue.models import Newspaper
import os 



class ClassifyPaperViewTestCase(NewspaperTestCase):
    def test_url(self):
    	# check the validity of url 
        paper_id = 1
        resp = self.client.get('/dashboard/classify_paper/%d' % paper_id)
        self.assertEqual(resp.status_code , 301)
        
class ClassifyTenderViewTestCase(TestCase):
    def test_url(self):
        tender_id = 1
        resp = self.client.get('/dashboard/classify_tender/%d' % tender_id)
        self.assertEqual(resp.status_code, 301)

class DeleteNewspaperViewTestCase(NewspaperTestCase):
    cp_paper = None
    paper_path2 = 'tests_/newspaper2.pdf'

    def setUp(self):
        super(DeleteNewspaperViewTestCase, self).setUp()
        self.cp_paper = Newspaper.objects.create(file=self.paper_path2)

    def test_delete(self):
        
        # copy file 
        src = self.paper.file.path
        target = self.cp_paper.file.path
        copyfile(src, target)

        self.assertTrue(os.path.isfile(target))        
        
        # test file
        resp = self.client.get('/dashboard/delete_newspaper/%d/' % self.cp_paper.id)
        exists = os.path.isfile(target)                 
        if exists: 
            os.remove(target)

        # test record 
        paper_exists  = Newspaper.objects.filter(id=self.cp_paper.id)

        self.assertEqual(len(paper_exists), 0)
        self.assertFalse(exists)



# class DeleteTenderViewTestCase(TenderTestCase):
#     cp_paper = None
#     paper_path2 = 'tests_/tender2.jpg'

#     def setUp(self):
#         super(DeleteTenderViewTestCase, self).setUp()
#         self.cp_paper = Snippet.objects.create(image=self.paper_path2)

#     def test_delete(self):
#         # copy file 
#         src = self.paper.file.path
#         target = self.cp_paper.file.path
#         copyfile(src, target)

#         self.assertTrue(os.path.isfile(target))        
        
#         resp = self.client.get('/dashboard/delete_tender/%d/' % self.cp_paper.id)
#         exists = os.path.isfile(target)         
        
#         if exists: 
#             os.remove(target)

#         self.assertFalse(exists)

