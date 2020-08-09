# Credential Escrow service

Allows credentials to be stored in such a way that they can be retrived once, and only once, with a one-time-password.

Intended use case for this was for systems that would eventually become untrusted and required credentials for initial setup/configuration but not on an ongoing basis. Specifically dedicated servers for Gaming.

Work flow:

* As part of the build process:
  * Set the credentials in SSM with OTP
  * Bakes the OTP into the application
* Application requests credentials from Credential Escrow using OTP
* Credential Escrow:
  * Verifies OTP
  * Gets credentials
  * Deletes credentials and OTP from SSM
  * Returns credentials to application
* Application does what it needs to do with credentials
