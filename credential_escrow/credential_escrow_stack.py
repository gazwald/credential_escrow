import os

from aws_cdk import core

import aws_cdk.aws_apigateway as apigateway
import aws_cdk.aws_lambda as aws_lambda


class CredentialEscrowStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define API and it's resources
        self.api = self.create_api()
        self.api_escrow = self.create_escrow_resource()

        # Define Lambdas and their integrations
        self.lambda_escrow_create = self.create_escrow_create_lambda()
        self.lambda_escrow_get = self.create_escrow_get_lambda()
        self.lambda_escrow_create_integration = self.create_escrow_create_integration()
        self.lambda_escrow_get_integration = self.create_escrow_get_integration()

        # Add Lambda Integrations to API Resources
        self.add_escrow_create_lambda_to_api()
        self.add_escrow_get_lambda_to_api()

    def create_api(self):
        return apigateway.RestApi(self, "credential-escrow-api")

    def create_escrow_resource(self):
        return self.api.root.add_resource("escrow")

    def create_escrow_create_lambda(self):
        return aws_lambda.Function(self, "escrow-create-lambda",
            code=aws_lambda.Code.from_asset(os.path.join(os.getcwd(), "lambda-escrow-create")),
            handler="app.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_6
        )        

    def create_escrow_get_lambda(self):
        return aws_lambda.Function(self, "escrow-get-lambda",
            code=aws_lambda.Code.from_asset(os.path.join(os.getcwd(), "lambda-escrow-get")),
            handler="app.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_6
        )        

    def create_escrow_create_integration(self):
        return apigateway.LambdaIntegration(self.lambda_escrow_create)

    def create_escrow_get_integration(self):
        return apigateway.LambdaIntegration(self.lambda_escrow_get)

    def add_escrow_create_lambda_to_api(self):
        self.api_escrow.add_method("POST", self.lambda_escrow_create_integration)

    def add_escrow_get_lambda_to_api(self):
        self.api_escrow.add_method("GET", self.lambda_escrow_get_integration)
        
