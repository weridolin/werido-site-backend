
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from oauth.v1.serializers import ApplicationSerializer,ApplicationBriefSerializer
from oauth.models import OauthApplicationModel,AccessTokenModel
from utils.http_ import HTTPResponse
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.views import APIView
from oauth2_provider.views.base import BaseAuthorizationView
from oauth2_provider.exceptions import OAuthToolkitError
from oauth2_provider.scopes import get_scopes_backend
from oauth2_provider.models import generate_client_secret
from rest_framework_simplejwt.authentication import JWTAuthentication
from oauth2_provider.settings import oauth2_settings
from time import timezone
import json
class ApplicationRegisterViews(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ApplicationSerializer
 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_secret = generate_client_secret()
        self.perform_create(serializer,request.user,client_secret=client_secret)
        headers = self.get_success_headers(serializer.data)
        payload =serializer.data
        payload.update({"client_secret":client_secret})
        return HTTPResponse(data=payload,message="create oauth apps success" ,app_code="oauth",headers=headers)

    def perform_create(self, serializer,user,client_secret):
        serializer.save(user=user,client_secret=client_secret,client_secret_src=client_secret)
    


class ApplicationResourceViews(ViewSet):

    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        page = request.data.get("page",1)
        per_page = request.data.get("per_page",20)
        query_set = OauthApplicationModel.objects.all()
        data = ApplicationSerializer(query_set,many=True).data
        return HTTPResponse(
            data=data,
            app_code="oauth"
        )

    def create(self, request):
        return HTTPResponse(
            code=-1,
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            message="method not allowed",
            app_code="oauth"
        )

    def retrieve(self, request, pk=None):
        if pk:
            try:
                record = OauthApplicationModel.objects.get(id=pk)
            except OauthApplicationModel.DoesNotExist:
                return HTTPResponse(
                    code=-1,
                    message="can not find application!",
                    status=status.HTTP_404_NOT_FOUND
                )
        data = ApplicationSerializer(record).data
        return HTTPResponse(
            data=data,
            app_code="oauth"
        )

    def update(self, request, pk=None):
        client_id = request.data.get("client_id",None)
        if not client_id:
            return HTTPResponse(
                code=-1,
                app_code="oauth",
                status=status.HTTP_400_BAD_REQUEST,
                message=f"client id must be None"
            )
        try:
            record:OauthApplicationModel  = OauthApplicationModel.objects.get(client_id=client_id)
            if record.user != request.user:
                return HTTPResponse(
                    code=-1,
                    status=status.HTTP_403_FORBIDDEN,
                    message="您无权进行该操作",
                    app_code="oauth"
                )                
            for k,v in request.data.items():
                if k=="client_secret":
                    record.client_secret,record.client_secret_src = v,v                    
                elif k!="client_id" and hasattr(record,k):
                    setattr(record,k,v)
            record.save()
            return HTTPResponse(
                code=-1,
                status=status.HTTP_200_OK,
                message="update success",
                app_code="oauth"
            )
        except OauthApplicationModel.DoesNotExist:
            return HTTPResponse(
                code=-1,
                app_code="oauth",
                status=status.HTTP_404_NOT_FOUND,
                message=f"can not find application by {client_id}"
            )

    def partial_update(self, request, pk=None):
        return HTTPResponse(
            code=-1,
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            message="method not allowed",
            app_code="oauth"
        )

    def destroy(self, request, pk=None):
        if pk:
            try:
                app:OauthApplicationModel = OauthApplicationModel.objects.get(pk=pk)
            except OauthApplicationModel.DoesNotExist:
                return HTTPResponse(
                    code=-1,
                    message="can not find application!",
                    status=status.HTTP_404_NOT_FOUND
                )
        if app.user == request.user or request.user.is_superuser :
            app.delete()
            return HTTPResponse(
                message="delete success",
                app_code="oauth"
            )        
        else:
            return HTTPResponse(
                message="您没有权限执行该操作",
                app_code="oauth",
                code=-1,
                status=status.HTTP_403_FORBIDDEN
            )
            

from rest_framework_simplejwt.exceptions import InvalidToken
class AuthorizationView(APIView,BaseAuthorizationView):
    authentication_classes=[JWTAuthentication]
    # permission_classes = []

    def get(self, request):
        """
            Return 获取授权页面
        """
        try:
            scopes, credentials = self.validate_authorization_request(request)
        except OAuthToolkitError as error:
            # 检验参数是否合法
            return HTTPResponse(
                status=error.oauthlib_error.status_code,
                message=error.oauthlib_error.description,
                code=-1,
                app_code="oauth"
            )
        all_scopes = get_scopes_backend().get_all_scopes()
        kwargs = dict()
        kwargs["scopes_descriptions"] = [all_scopes[scope] for scope in scopes]
        kwargs["scopes"] = scopes
        # at this point we know an Application instance with such client_id exists in the database

        # TODO: Cache this!
        application = OauthApplicationModel.objects.get(client_id=credentials["client_id"])
        kwargs["application"] = ApplicationBriefSerializer(application).data
        kwargs["client_id"] = credentials["client_id"]
        kwargs["redirect_uri"] = credentials["redirect_uri"]
        kwargs["response_type"] = credentials["response_type"]
        kwargs["state"] = credentials["state"]
        if "code_challenge" in credentials:
            kwargs["code_challenge"] = credentials["code_challenge"]
        if "code_challenge_method" in credentials:
            kwargs["code_challenge_method"] = credentials["code_challenge_method"]
        if "nonce" in credentials:
            kwargs["nonce"] = credentials["nonce"]
        if "claims" in credentials:
            kwargs["claims"] = credentials["claims"]
        # # Check to see if the user has already granted access and return
        # # a successful response depending on "approval_prompt" url parameter
        require_approval = request.query_params.get("approval_prompt", oauth2_settings.REQUEST_APPROVAL_PROMPT)

        try:
            if require_approval == "auto":
                tokens = (AccessTokenModel.objects.filter(user=request.user, application=application, expires__gt=timezone.now()).all())
                # check past authorizations regarded the same scopes as the current one
                for token in tokens: 
                    if token.allow_scopes(scopes):
                        ## 生成对应的网关记录
                        uri, headers, body, status = self.create_authorization_response(
                            request=self.request,
                            scopes=" ".join(scopes),
                            credentials=credentials,
                            allow=True,
                        )
                        return HTTPResponse(
                            data={
                                "redirect_uri":uri,
                                "header":headers,
                                "body":body,
                            },
                            code=-1,
                            app_code="oauth",
                            status=status  
                        )
            # If skip_authorization field is True, skip the authorization screen even
            # if this is the first use of the application and there was no previous authorization.
            # This is useful for in-house applications-> assume an in-house applications are already approved.
            # ## TODO 这里是跳过授权界面。那user???
            # elif application.skip_authorization:
            ## 生成对应的网关记录
            uri, headers, body, status = self.create_authorization_response(
                request=self.request, scopes=" ".join(scopes), credentials=credentials, allow=True
            )
            return HTTPResponse(
                data={
                    "redirect_uri":uri,
                    "header":headers,
                    "body":body,
                },
                code=-1,
                app_code="oauth",
                status=status  
            )
            # else:


        except OAuthToolkitError as error:
            return HTTPResponse(
                status=error.oauthlib_error.status_code,
                message=error.oauthlib_error.description,
                code=-1,
                app_code="oauth"
            )


from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework.decorators import action

from oauth.v1.signals import app_authorized
class TokenAccessViews(OAuthLibMixin,APIView):
    authentication_classes =[]
    permission_classes =[]
    
    def post(self,request):
        ### 根据凭证生成对应的access token/refresh token 同时会去删除grant表里面的记录
        url, headers, body, status = self.create_token_response(request)
        print(">>> get access token",headers,body,status,url)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = AccessTokenModel.objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
            return HTTPResponse(
                data=json.loads(body),
                status=status,
                headers=headers
            )
        else:
            return HTTPResponse(
                code=-1,
                message=json.loads(body).get("error","a undefined error happen!"),
                app_code="oauth"
            )


class RevokeTokenViews(OAuthLibMixin,APIView):
    authentication_classes=[]
    permission_classes = []

    def post(self,request):
        url, headers, body, _status = self.create_revocation_response(request)
        print(headers,body,_status,">>>")
        if _status == 200:
            return HTTPResponse(
                status=status.HTTP_204_NO_CONTENT,
                headers=headers
            )
        else:
            return HTTPResponse(
                code=-1,
                message=json.loads(body).get("error","a undefined error happen!"),
                app_code="oauth"
            )

from authentication.models import UserProfile
from authentication.v1.serializers import UserProfileSerializer
class UserInfoByOauthViews(OAuthLibMixin,APIView):
    authentication_classes=[]
    permission_classes = []

    def get(self,request):
        # print(request.META)
        request.META["Authorization"] = request.META["HTTP_AUTHORIZATION"]
        _status,request = self.verify_request(request)
        if not _status:
            return HTTPResponse(
                code=-1,
                status=status.HTTP_401_UNAUTHORIZED,
                message="access token is invalid or expired",
                app_code="oauth"
            )
        else:
            try:
                user_profile = UserProfile.objects.get(user=request.user)
                return HTTPResponse(
                    data=UserProfileSerializer(user_profile).data,
                    app_code="oauth"
                )
            except UserProfile.DoesNotExist:
                return HTTPResponse(
                    code=-1,
                    status=status.HTTP_404_NOT_FOUND,
                    message="can not find profile",
                    app_code="oauth"
                )

