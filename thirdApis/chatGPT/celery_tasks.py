from core.celery import app
from thirdApis.models import ChatGPTMessage,ChatGPTConversation

@app.task(name="celeryTask.chatGPT.clearMessage")
def clear_message(conversation_id):
    if isinstance(conversation_id,str):
        conversation_id = int(conversation_id)
    if isinstance(conversation_id,list):
        messages = ChatGPTMessage.objects.filter(conversation_id__in=conversation_id).all()
        messages.delete()
    elif isinstance(conversation_id,int):
        messages = ChatGPTMessage.objects.filter(conversation_id=conversation_id).all()
        messages.delete()