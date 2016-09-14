# -*- coding: utf-8 -*-#
__author__ = 'AMA'

import lxml.html as html
from urllib.request import urlopen, urlretrieve
from urllib.parse   import urlsplit
from .models import StatMsg

def singleGrab( url ):
    h1=''
    msg=''
    title= ''

    try:
        page = html.parse(urlopen(url))
        base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
    except:
        msg = 'Error open URL'
        sm = StatMsg(parsingURL=url, msg=msg)
        sm.save()
    else:
        msg = 'Parsing done'
        sm = StatMsg(parsingURL=url, msg=msg)
        sm.save()

        try:
            title = page.xpath("//title/text()")[0]
        except: msg = 'Error parsing TITLE'
        else:   msg = 'Parsing TITLE is OK'
        finally:
            sm = StatMsg(parsingURL=url, msg=msg)
            sm.save()

        try:
            h1 = page.xpath("//h2[1]/text()")[0]
        except: msg = 'Error parsing H1'
        else:   msg = 'Parsing H1 is OK'
        finally:
            sm = StatMsg(parsingURL=url, msg=msg)
            sm.save()

        try:
            imgurl = page.xpath('//img/@src')[0]
        except: msg = 'Error parsing IMG'
        else:
                msg = 'Parsing IMG is OK'
                simg = imgurl.split('/')
                fileName = simg[len(simg) - 1]
                if base_url not in imgurl:
                    imgurl = base_url + imgurl
                urlretrieve(imgurl, fileName)
        finally:
            sm = StatMsg(parsingURL=url, msg=msg)
            sm.save()

    finally:
        return url, msg, title, h1

