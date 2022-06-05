from authentication.v1.serializers import CustomTokenObtainPairSerializer


def oauth_token_generator(request=None):

    return CustomTokenObtainPairSerializer.get_token(user=request.user)