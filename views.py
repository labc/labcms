from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect

import yaml, markdown, codecs

class StaticPage(object):
	"""
	Handles all the static page parsing, loading, etc. Lots of nuts & bolts.
	"""
	text = None
	meta = None
	document = None
	
	def __init__(self, fn=None):
		"""StaticPage(string|file)
		StaticPage()
		
		Loads data. First form from given file).
		"""
		if fn is not None:
			if typeof(fn, basestring):
				f = codecs.open(fn, mode="r", encoding="utf-8")
			else:
				f = fn
			self.loadFile(f):
	
	def loadFile(self, file):
		"""sp.loadFile(file)
		Loads data from the given file-like object.
		"""
		
		lines = iter(file)
		l = lines.next()
		yamldata = ''
		mddata = ''
		if l.strip() == u'---':
			for l in lines:
				if l.strip() == u'---':
					break
				yamldata += l
			l = lines.next()
		
		# At this point, l contains the first line of Markdown text
		mddata = l
		for l in lines:
			mddata += l
		
		self.meta = yaml.load(yamldata)
		self.text = mddata
		self.document = markdown.markdown(self.text)

def render(request, url):
	"""
	Entry point for views.
	"""
	pass
	
def findtemplate(url):
	pass

