from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import SendMessageSerializer
import requests


# Abilito il metodo post e l'accesso se autenticati. Scrivo una vista funzione perché
# una classe dovrei comunque modificarla molto.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message_view(request):
    if not request.user.is_authenticated:
        return Response({"result": "Error sending telegram message", "errors": 'aiai'},
                        status=status.HTTP_400_BAD_REQUEST)
    bot_token = '<token>'
    bot_chat_id = '<il tuo chat id>' # Scrivendo al bot /chatinfo fornisce l'id della chat

    serializer = SendMessageSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=False):
        # In caso di errori di validazione li segnalo nella risposta
        errors = []
        for key, values in serializer.errors.items():
            errors = [f'{key}: {value[:]}' for value in values]
        return Response({"result": "Error sending telegram message", "errors": errors},
                        status=status.HTTP_400_BAD_REQUEST)

    api_errors = []

    # Se nella richiesta c'è un testo lo invio
    if "text" in request.data.keys():
        bot_message = f'{request.data["text"]}'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
        if response.status_code != 200:
            api_errors.append(f'TelegramAPI error {response.status_code}: can not send test')

    # Se nelle richiesta c'è una immagine la invio
    if "image" in request.data.keys():
        bot_image = {'photo': request.data["image"]}
        send_image = 'https://api.telegram.org/bot' + bot_token + '/sendPhoto?chat_id=' + bot_chat_id + '?photo=files'
        response = requests.get(send_image, files=bot_image)
        if response.status_code != 200:
            api_errors.append(f'TelegramAPI error {response.status_code}: can not send image')

    # Se durante l'invio si sono verificati errori la risposta ci avverte di quali sono stati fornendo il codice
    if api_errors:
        return Response({"result": "Error sending telegram message", "errors": api_errors},
                        status=status.HTTP_400_BAD_REQUEST)

    # Se tutto è andato liscio ci dà il messaggio di successo
    return Response({"result": "Message successfully sent"})


