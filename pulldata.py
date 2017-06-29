import re
import lxml.html
import sitemaptools
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def remove_http(name_string):
    if name_string.startswith("https"):
        return str(name_string).lstrip("https://")
    elif name_string.startswith("http"):
        return str(name_string).lstrip("http://")
    else:
        return name_string


def replace_bad_chars(name_string):
    return re.sub('[^\w\-_\. ]', '', remove_http(name_string))


def get_anchor_list(site):
    page = lxml.html.parse(urlopen(site)).getroot()
    html_anchor_elements = page.cssselect('a')  # html anchor element
    return html_anchor_elements


def get_img_list(site):
    page = lxml.html.parse(site).getroot()
    html_img_elements = page.cssselect('img')
    return html_img_elements


def get_element_base(html_element):
    return html_element.base


def get_link_source(anchor):
    if anchor.get_title() is not None and anchor.get_title() is not "":
        return anchor.get_title()
    elif anchor.get_name() is not None and anchor.get_name() is not "":
        return anchor.get_name()
    elif anchor.get_element().getchildren() is not [] and 'img' in anchor.get_element().attrib:
        for h in anchor.get_element().getchildren():
            o = Img(h)
            return "IMG: SRC = " + o.get_src()
    else:
        return lxml.html.HtmlElement.findtext(lxml.html.HtmlElement.getparent(anchor.get_element()), 'a')


class Site:
    def __init__(self, url):
        self.__url = url
        self.__anchor_list = get_anchor_list(self.__url)
        try:
            self.__parsed = lxml.html.parse(urlopen(self.__url)).getroot()
        except HTTPError:
            self.__parsed = None

    def get_anchor_list(self):
        return self.__anchor_list

    def get_url(self):
        return self.__url


class HTMLElement:
    def __init__(self, element):
        self.__attribute_dict = sitemaptools.CaseInsensitiveDict(element.attrib)


class Anchor(HTMLElement):
    """
	Python representation of html anchor element. Includes functions for extracting various element attributes:

	href:	<h>ypertext <ref>erence; References a network address or network address + reference
			(ie. href=#identifier allows an html element in the current page to be directly referenced. Following the
			hypertext loads the page scrolled to the element referenced by the identifier.

	name:	Identifier for the anchor; Allows href to reference this anchor within the html document using hashtag
			notation (#identifier). Names within the same document must be unique.

	rel:	<rel>ationship; Comma-separated list of relationship values:
				UseIndex, UseGlossary, Annotation, Reply, Embed, Precedes, Subdocument, Present, Search, Supersedes,
				History, Made, Owns, Approves, Supports, Refutes, Includes, Interested

	rev:	<rev>erse relationship; Same as rel, but relationship semantics are reversed.

	urn:	<u>niform <r>esource <n>ame; Value references the URN for the document (such as a book's ISBN)

	title:	Title of the document; String representing the title of the document referenced by href.

	methods:String list of HTTP methods supported by the object for public use:
				GET, HEAD, POST, PUT, DELETE, CONNECT, OPTIONS, TRACE, PATCH
	"""

    def __init__(self, element):
        HTMLElement.__init__(self, element)
        self.__element = element
        self.__attribute_dict = sitemaptools.CaseInsensitiveDict(element.attrib)

    def get_element(self):
        return self.__element

    def get_href(self):
        if "href" in self.__attribute_dict:
            if not str(self.__attribute_dict["href"]).startswith("http"):
                return lxml.html.urljoin(get_element_base(self.__element), str(self.__attribute_dict["href"]))
            else:
                return self.__attribute_dict["href"]
        else:
            return ""

    def get_name(self):
        if "name" in self.__attribute_dict:
            return self.__attribute_dict["name"]
        else:
            return ""

    def get_rel(self):
        if "rel" in self.__attribute_dict:
            return self.__attribute_dict["rel"]
        else:
            return ""

    def get_rev(self):
        if "rev" in self.__attribute_dict:
            return self.__attribute_dict["rev"]
        else:
            return ""

    def get_urn(self):
        if "urn" in self.__attribute_dict:
            return self.__attribute_dict["urn"]
        else:
            return ""

    def get_title(self):
        if "title" in self.__attribute_dict:
            return self.__attribute_dict["title"]
        else:
            return ""

    def get_methods(self):
        if "methods" in self.__attribute_dict:
            return self.__attribute_dict["methods"]
        else:
            return ""

    def get_attributes(self):
        return self.__attribute_dict

    def get_children(self):
        return self.__element.getchildren()

    def get_parent(self):
        return self.__element.getparent()


class Img(HTMLElement):
    def __init__(self, element):
        HTMLElement.__init__(self, element)
        self.__parent = lxml.html.HtmlElement.getparent(element)
        self.__element = element
        self.__attribute_dict = element.attrib

    def get_parent(self):
        return self.__parent

    def get_src(self):
        if 'src' in self.__attribute_dict:
            return self.__attribute_dict['src']
        else:
            return ""


class SiteMap:
    def __init__(self, url, levels=2, internal=True, ignored=list()):
        self.__levels = levels
        self.__url = url
        self.__internal = internal
        self.__ignored = ignored
        self.__site = Site(url)

    def get_url(self):
        return self.__url

    def get_levels(self):
        return self.__levels

    def get_site(self):
        return self.__site

    def get_site_filename(self):
        return replace_bad_chars(str(self.__url) + ".txt")

    def map_site(self, url, level):
        fn = self.get_site_filename()
        if level != 0:
            f = open(fn, 'a')
            for anchor in Site(url).get_anchor_list():
                link = Anchor(anchor).get_href()
                source = get_link_source(Anchor(anchor))
                if link not in open(fn).read() and not str(get_element_base(Anchor(anchor).get_element())).__contains__('facebook')and not str(get_element_base(Anchor(anchor).get_element())).__contains__('twitter'):
                    f.write(str(source) + " --> " + link + '\n')
                    self.map_site(link, level - 1)
            f.close()
        else:
            pass


if __name__ == '__main__':
    a = SiteMap("http://jmaa.com")
    a.map_site(a.get_url(), 3)
