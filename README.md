# Azure VM REST API DEMO

This code demonstrates how a Web application can authenticate users and call a downstream API using the signed in user's token

This code is based on: https://github.com/Azure-Samples/ms-identity-python-webapp

The demo uses the Microsoft Identity Platform and the Microsoft Authentication Library(MSAL) for Python to manage user authentication. 

To call azure management APIs, the app obtains an access token for the user with the scope "https://management.azure.com/user_impersonation". This allows the app to impersonate the user in the downstream API requests to Azure Management API. 
```
 token = auth.get_token_for_user(["https://management.azure.com/user_impersonation"])
```
## Instructions
1. Create an app registration in Azure AD and give it the API permission user_impersonation for management.azure.com

2. Create a client secret in the app registration.
   
3. Clone the repository or download it to your local environment
   ```
   PS > git clone git@github.com:aminsrc/azure-vms-rest-api-demo.git
   ```
4. In the root folder of the repository, create a python virtual environment, activate it, and pip install requirements
    ```
    PS > cd azure-vms-rest-api-demo
    PS > virtualenv.exe venv
    PS > .\venv\Scripts\activate
    PS > pip install -r requirements.txt
    ```

5. Set the following environment variables:

    ```
    PS > $env:CLIENT_ID=<Your App registration Client ID>
    PS > $env:CLIENT_SECRET=<Your app registration client secret>
    PS > $env:SUBSCRIPTION_ID=<Your subscription>
    PS > $env:TENANT_ID=<Your tenant-ID>
    ```
6. Run the app
   ```
   PS > python.exe .\app.py
   ```


