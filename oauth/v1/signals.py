from oauth2_provider.signals import app_authorized


def handle_app_authorized_signal(sender,request,token,**kwargs):
    print(">>> access token",sender,request,token)


app_authorized.connect(handle_app_authorized_signal)