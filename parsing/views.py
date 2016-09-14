from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import StatMsg, QueneURLs
from .serializers import StatMsgSerializer, QueneMsgSerializer
from concurrent import futures
from .parsing import *


@csrf_exempt # We don't need CSRF token
@api_view(['GET'])
def statMsgList(request):
    try:
        statMsgs = StatMsg.objects.all()
    except:
        print('err')
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
def startParsing(request):
    print('-------------')
    urls=[]
    records = QueneURLs.objects.all()
    for url in records:
        urls.append(url.parsingURL )
    print(urls)
    with futures.ThreadPoolExecutor(5) as executor:
        res = executor.map( singleGrab, urls )

    for r in res:
        print(r[0],r[1])


    return Response("parsing weel done", status=status.HTTP_201_CREATED)
