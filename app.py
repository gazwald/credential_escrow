#!/usr/bin/env python3

from aws_cdk import core

from credential_escrow.credential_escrow_stack import CredentialEscrowStack


app = core.App()
CredentialEscrowStack(app, "credential-escrow")

app.synth()
