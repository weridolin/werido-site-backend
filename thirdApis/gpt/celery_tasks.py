from core.celery import app
from thirdApis.models import GptMessage,GptConversation


### 删除会话时异步删除会话里面的消息
@app.task(
    name="celeryTask.Gpt.clearMessage",
    queue="site",
    retry=True, 
    retry_policy={
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
})
def clear_message(conversation_id):
    print(">>> clear message",conversation_id)
    if isinstance(conversation_id,str):
        conversation_id = int(conversation_id)
    if isinstance(conversation_id,list):
        messages = GptMessage.objects.filter(conversation_id__in=conversation_id).all()
        messages.delete()
    elif isinstance(conversation_id,int):
        messages = GptMessage.objects.filter(conversation_id=conversation_id).all()
        messages.delete()