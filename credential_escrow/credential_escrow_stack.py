import os

from aws_cdk import core

import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_lambda as aws_lambda


class CredentialEscrowStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.api = self.create_api()
        self.api_otp = self.create_otp_resource()
        self.api_escrow = self.create_escrow_resource()
        self.lambda_otp = self.create_otp_lambda()
        self.lambda_escrow = self.create_escrow_lambda()
        self.lambda_otp_integration = self.create_otp_integration()
        self.lambda_escrow_integration = self.create_escrow_integration()
        self.add_otp_lambda_to_api()
        self.add_escrow_lambda_to_api()

    def create_api(self):
        return apigateway.RestApi(self, "credential-escrow-api")

    def create_otp_resource(self):
        return self.api.root.add_resource("otp")

    def create_escrow_resource(self):
        return self.api.root.add_resource("escrow")

    def create_otp_lambda(self):
        return aws_lambda.Function(self, "otp-lambda",
            code=aws_lambda.Code.from_asset(os.path.join(os.getcwd(), "otp-lambda")),
            handler="app.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_6
        )

    def create_escrow_lambda(self):
        return aws_lambda.Function(self, "escrow-lambda",
            code=aws_lambda.Code.from_asset(os.path.join(os.getcwd(), "escrow-lambda")),
            handler="app.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_6
        )        

    def create_otp_integration(self):
        return apigateway.LambdaIntegration(self.lambda_otp)

    def create_escrow_integration(self):
        return apigateway.LambdaIntegration(self.lambda_escrow)

    def add_otp_lambda_to_api(self):
        self.api_otp.add_method("GET", self.lambda_otp_integration)

    def add_escrow_lambda_to_api(self):
        self.api_escrow.add_method("GET", self.lambda_escrow_integration)
        
