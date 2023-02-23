import os

CLIENT_ID = os.getenv("CLIENT_ID")
if not CLIENT_ID:
    raise ValueError("Need to define CLIENT_ID environment variable")

CLIENT_SECRET = os.getenv("CLIENT_SECRET")
if not CLIENT_SECRET:
    raise ValueError("Need to define CLIENT_SECRET environment variable")

SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
if not SUBSCRIPTION_ID:
    raise ValueError("Need to define SUBSCRIPTION_ID environment variable")

TENANT_ID = os.getenv("TENANT_ID")
if not TENANT_ID:
    raise ValueError("Need to define TENANT_ID environment variable")


AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
                              # The absolute URL must match the redirect URI you set
                              # in the app's registration in the Azure portal.

# You can find more Microsoft Graph API endpoints from Graph Explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer
ENDPOINT = 'https://graph.microsoft.com/v1.0/users'  # This resource requires no admin consent

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
SCOPE = ["https://management.azure.com/user_impersonation"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session
