from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import StatMsgSerializer, QueneMsgSerializer, ScheduleQueneSerializer
from concurrent import futures
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import lxml.html as html
from urllib.request import urlopen, urlretrieve
from urllib.parse   import urlsplit
from .models import StatMsg, ParsingData, QueneURLs, ScheduleQuene
from testjob2.settings import  BASE_DIR, STATIC_URL
import datetime
import re
import time
import pytz

pendingFlag = True

@csrf_exempt # We don't need CSRF token
@api_view(['GET'])
def statMsgList(request):
    try:
        statMsgs = StatMsg.objects.all()
    except:
        print('Error in StatMsgDB')
        return Response('', status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = StatMsgSerializer(statMsgs, many=True)
        for msg in statMsgs: msg.delete()
        return Response(serializer.data)



@csrf_exempt # We don't need CSRF token
@api_view(['POST'])
def queneList(request):
    serializer = QueneMsgSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        sm = StatMsg( parsingURL=serializer.data['parsingURL'], msg='URL added to quene' )
        sm.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt # We don't need CSRF token
@api_view(['POST'])
def scheduleParsing( request ):

    a=ScheduleQuene.objects.all()
    a.delete()
    serializer = ScheduleQueneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        sm = StatMsg(parsingURL='No URL', msg='DATATIME set')
        sm.save()
        print( 'raw', serializer.data['strDataTime'])
        dt = datetime.datetime.strptime( serializer.data['strDataTime'], "%Y-%m-%dT%H:%M")
        arg = ( dt, request )
        print('Calling scheduler on ', arg[0], 'time')
        with futures.ThreadPoolExecutor(6) as executor:
            executor.submit(scheduler, arg )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt # We don't need CSRF token
@api_view(['POST'])
def stopParsing(request):
    global pendingFlag
    print('Parsing STOPPED')

    pendingFlag = False
    msg = 'Parsing STOPPED'
    sm = StatMsg(parsingURL="NO URL", msg=msg)
    sm.save()

    return Response("STOP parsing weel done", status=status.HTTP_100_CONTINUE )

@csrf_exempt # We don't need CSRF token
@api_view(['POST'])
def startParsing(request):
    global pendingFlag
    print('Parsing STARTED')

    pendingFlag = True
    msg = 'Parsing STARTED'
    sm = StatMsg(parsingURL="NO URL", msg=msg)
    sm.save()

    urls = []
    records = QueneURLs.objects.all()
    for rec in records:
        urls.append((rec.parsingURL, rec.id))

    with futures.ThreadPoolExecutor(6) as executor:
        myfutures = [executor.submit(singleGrab, url) for url in urls]

    return Response("START parsing weel done", status=status.HTTP_100_CONTINUE )

class ParsingDataDetailView(DetailView):

    model = ParsingData
    context_object_name = 'parsingDATA'

    def get_object(self):
        object = super().get_object()
        self.id = object.id
        return object

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        nextData = ParsingData.objects.get(id=self.id+1 )
        context['id2'] = nextData.id
        context['parsingURL2']=nextData.parsingURL
        context['title2'] = nextData.title
        context['h12'] = nextData.h1
        context['source_image_url2'] = nextData.source_image_url
        context['image_url2'] = nextData.image_url

        nextData = ParsingData.objects.get(id=self.id + 2)
        context['id3'] = nextData.id
        context['parsingURL3'] = nextData.parsingURL
        context['title3'] = nextData.title
        context['h13'] = nextData.h1
        context['source_image_url3'] = nextData.source_image_url
        context['image_url3'] = nextData.image_url

        return context

class ParsingDataListView(ListView):

    model = ParsingData
    context_object_name = 'parsingDATA'


def singleGrab(arg):
    if pendingFlag:
        h1 = ''
        msg = ''
        title = ''
        url = arg[0]
        id = arg[1]

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
            except:
                msg = 'Error parsing TITLE'
            else:
                msg = 'Parsing TITLE is OK'
            finally:
                sm = StatMsg(parsingURL=url, msg=msg)
                sm.save()

            try:
                h1 = page.xpath("//h1[1]/text()")[0]
            except:
                msg = 'Error parsing H1'
            else:
                msg = 'Parsing H1 is OK'
            finally:
                sm = StatMsg(parsingURL=url, msg=msg)
                sm.save()

            try:
                imgurl = page.xpath('//img/@src')[0]

            except:
                msg = 'Error parsing IMG'
            else:
                msg = 'Parsing IMG is OK'
                simg = imgurl.split('/')
                fileName = simg[len(simg) - 1]
                if '//' not in imgurl:
                    imgurl = base_url + imgurl

                imgurl = re.sub("/\.\./", '/', imgurl)
                if imgurl[0] == '/' and imgurl[1] == '/':
                    imgurl = 'http:' + imgurl

                image_url = BASE_DIR + STATIC_URL + fileName

                try:
                    urlretrieve(imgurl, image_url)
                except:
                    image_url = ''

            finally:
                sm = StatMsg(parsingURL=url, msg=msg)
                sm.save()

            pr = ParsingData(parsingURL=url, title=title, h1=h1, source_image_url=imgurl, image_url=image_url)
            pr.save()

            msg = "Parsing URL data stored to DB"
            sm = StatMsg(parsingURL=url, msg=msg)
            sm.save()
            print(msg)

        finally:
            q = QueneURLs.objects.get(pk=id)
            q.delete()
            msg = "URL parced and deleted"
            sm = StatMsg(parsingURL=url, msg=msg)
            sm.save()


def scheduler( arg ):
        print ('Scheduler started ')

        msg = "Scheduler started "
        tz = pytz.timezone('Europe/Moscow')

        sm = StatMsg(parsingURL='No URL', msg=msg)
        sm.save()

        while True:
            now_time = datetime.datetime.now(tz)
            s = now_time.strftime("%Y-%m-%dT%H:%M")
            now_time = datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M")

            time.sleep(1)

            if now_time > arg[0]:
                startParsing( arg[1])
                return

