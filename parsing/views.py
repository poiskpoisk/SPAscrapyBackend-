from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import StatMsg
from .serializers import StatMsgSerializer, QueneMsgSerializer

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


@api_view(['POST'])
def queneList(request):
    serializer = QueneMsgSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        sm = StatMsg( parsingURL=serializer.data['parsingURL'], msg='URL added to quene' )
        sm.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
