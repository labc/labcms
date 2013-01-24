from django.template import loader, RequestContext
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.conf import settings
from django.utils.safestring import mark_safe

import markdown, codecs, os

class StaticPage(object):
	"""
	Handles all the static page parsing, loading, etc. Lots of nuts & bolts.
	"""
	text = None
	meta = None
	document = None
	
	def __init__(self, fn=None, **kwargs):
		"""StaticPage(string|file)
		StaticPage()
		
		Loads data. First form from given file).
		"""
		self._title = None
		if fn is not None:
			if typeof(fn, basestring):
				self._title = os.path.basename(fn)
				f = codecs.open(fn, mode="rU", encoding="utf-8")
			else:
				f = fn
				if hasattr(f, 'name')
					self._title = os.path.basename(f.name)
			
			self.loadFile(f):
		
		if 'name' in kwargs:
			self._title = os.path.basename(kwargs['name'])
		if 'title' in kwargs:
			self._title = kwargs['title']
	
	def loadFile(self, file):
		"""sp.loadFile(file)
		Loads data from the given file-like object.
		"""
		
		self.text = file.read()
		md = markdown.Markdown(extensions=['meta']) #TODO: Add extensions as a configuration option
		self.document = md.convert(self.text)
		self.meta = md.Meta

def findpage(url):
	"""findpage(string) -> StaticPage
	Returns the StaticPage for the given URL, or raises Http404
	"""
	if url[0] == '/':
		url = url[1:]
	
	# Remove queries
	if '?' in url:
		i = url.find('?')
		url = url[:i]
	
	# Just flat-out don't allow current directory or parent directory
	if url[:2] == './'  or  '/./' in url or url[-2] == '/.':
		raise Http404
	if url[:3] == '../' or '/../' in url or url[-2] == '/..':
		raise Http404
	
	for pagedir in config.STATICPAGES_DIRS:
		fn = os.path.join(pagedir, url)
		if os.path.exist(fn):
			return StaticPage(fn)
	else:
		raise Http404
	

def render(request, url):
	"""
	Entry point for views.
	"""
	page = findpage(url)
	
	c = RequestContext(request, {
        'data': page.meta,
        'text': mark_safe(page.document),
    })
    
    if 'template' in page.meta:
        t = loader.select_template((page.meta['template'], config.STATIC_TEMPLATE))
    else:
        t = loader.get_template(config.STATIC_TEMPLATE)
    
    response = HttpResponse(t.render(c))
	return response
