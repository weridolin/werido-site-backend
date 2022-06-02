
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from oauth.v1.serializers import ApplicationSerializer
from oauth.models import OauthModel
from utils.http_ import HTTPResponse
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework import status
from rest_framework.views import APIView
from oauth2_provider.views.base import BaseAuthorizationView

class ApplicationRegisterViews(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ApplicationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer,request.user)
        headers = self.get_success_headers(serializer.data)
        return HTTPResponse(data=serializer.data,message="create oauth apps success" ,app_code="oauth",headers=headers)

    def perform_create(self, serializer,user):
        serializer.save(user=user)
    


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
        query_set = OauthModel.objects.all()
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
                record = OauthModel.objects.get(id=pk)
            except OauthModel.DoesNotExist:
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
        return HTTPResponse(
            code=-1,
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            message="method not allowed",
            app_code="oauth"
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
                app:OauthModel = OauthModel.objects.get(pk=pk)
            except OauthModel.DoesNotExist:
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
            


class AuthorizationView(APIView,BaseAuthorizationView):
    authentication_classes=[IsAuthenticated]

    def get(self, request, format=None):
        """
            Return 获取授权页面
        """

        try:
            scopes, credentials = self.validate_authorization_request(request)
        except OAuthToolkitError as error:
            # Application is not available at this time.
            return self.error_response(error, application=None)

        all_scopes = get_scopes_backend().get_all_scopes()
        kwargs["scopes_descriptions"] = [all_scopes[scope] for scope in scopes]
        kwargs["scopes"] = scopes
        # at this point we know an Application instance with such client_id exists in the database

        # TODO: Cache this!
        application = get_application_model().objects.get(client_id=credentials["client_id"])

        kwargs["application"] = application
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
            kwargs["claims"] = json.dumps(credentials["claims"])

        self.oauth2_data = kwargs
        # following two loc are here only because of https://code.djangoproject.com/ticket/17795
        form = self.get_form(self.get_form_class())
        kwargs["form"] = form

        # Check to see if the user has already granted access and return
        # a successful response depending on "approval_prompt" url parameter
        require_approval = request.GET.get("approval_prompt", oauth2_settings.REQUEST_APPROVAL_PROMPT)

        try:
            # If skip_authorization field is True, skip the authorization screen even
            # if this is the first use of the application and there was no previous authorization.
            # This is useful for in-house applications-> assume an in-house applications
            # are already approved.
            if application.skip_authorization:
                uri, headers, body, status = self.create_authorization_response(
                    request=self.request, scopes=" ".join(scopes), credentials=credentials, allow=True
                )
                return self.redirect(uri, application)

            elif require_approval == "auto":
                tokens = (
                    get_access_token_model()
                    .objects.filter(
                        user=request.user, application=kwargs["application"], expires__gt=timezone.now()
                    )
                    .all()
                )

                # check past authorizations regarded the same scopes as the current one
                for token in tokens:
                    if token.allow_scopes(scopes):
                        uri, headers, body, status = self.create_authorization_response(
                            request=self.request,
                            scopes=" ".join(scopes),
                            credentials=credentials,
                            allow=True,
                        )
                        return self.redirect(uri, application)

        except OAuthToolkitError as error:
            return self.error_response(error, application)

        return self.render_to_response(self.get_context_data(**kwargs))
    

