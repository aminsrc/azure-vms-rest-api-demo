from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
import identity, identity.web
import requests
import app_config
import msal
import uuid

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

auth = identity.web.Auth(
    session=session,
    authority=app.config.get("AUTHORITY"),
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
    )

@app.route("/login")
def login():
    return render_template("login.html", version=identity.__version__, **auth.log_in(
        scopes=app_config.SCOPE,  # Have user consent scopes during log-in
        redirect_uri=url_for("auth_response", _external=True),  # Optional. If present, this absolute URL must match your app's redirect_uri registered in Azure Portal
        ))

@app.route(app_config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    return render_template("auth_error.html", result=result) if "error" in result else redirect(url_for("index"))

@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))

@app.route("/")
def index():
    if not auth.get_user():
        return redirect(url_for("login"))
    return render_template('index.html', user=auth.get_user(), version=identity.__version__)


@app.route('/list_vms')
def list_vms():
    token = auth.get_token_for_user(["https://management.azure.com/user_impersonation"])
    if "error" in token:
        return redirect(url_for("login"))
    subscriptionId = app.config['SUBSCRIPTION_ID']
    resourceGroupName = "vm-management-demo"

    list_vms_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines?api-version=2022-11-01"
    
    vms = requests.get(  # Use token to call downstream api
        list_vms_endpoint,
        headers={
            'Authorization': 'Bearer ' + token['access_token']
            }
        ).json()

    vm_names = [vm['name'] for vm in vms['value']]
   
    return render_template('display.html', vm_names=vm_names)

@app.route('/start_vm/<vm_name>')
def start_vm(vm_name):
    token = auth.get_token_for_user(["https://management.azure.com/user_impersonation"])
    if "error" in token:
        return redirect(url_for("login"))
    subscriptionId = app.config['SUBSCRIPTION_ID']
    resourceGroupName = "vm-management-demo"
    vmName = vm_name
    start_vm_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/start?api-version=2022-11-01"

    api_result = requests.post(  # Use token to call downstream api
        start_vm_endpoint,
        headers={
            'Authorization': 'Bearer ' + token['access_token']
            }
        )
    
    if api_result.status_code == 202:
        return f"Starting VM {vm_name}"



@app.route('/stop_vm/<vm_name>')
def stop_vm(vm_name):
    token = auth.get_token_for_user(["https://management.azure.com/user_impersonation"])
    if "error" in token:
        return redirect(url_for("login"))
    subscriptionId = app.config['SUBSCRIPTION_ID']
    resourceGroupName = "vm-management-demo"
    vmName = vm_name
    stop_vm_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/powerOff?api-version=2022-11-01"

    api_result = requests.post(  # Use token to call downstream api
        stop_vm_endpoint,
        headers={
            'Authorization': 'Bearer ' + token['access_token']
            }
        )
    
    if api_result.status_code == 202:
        return f"Stopping VM {vm_name}"


@app.route('/vm_status/<vm_name>')
def get_vm_status(vm_name):
    token = auth.get_token_for_user(["https://management.azure.com/user_impersonation"])
    if "error" in token:
        return redirect(url_for("login"))
    subscriptionId = app.config['SUBSCRIPTION_ID']
    resourceGroupName = "vm-management-demo"
    vmName = vm_name
    vm_status_endpoint = f"https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Compute/virtualMachines/{vmName}/instanceView?api-version=2022-11-01"

    api_result = requests.get(  # Use token to call downstream api
        vm_status_endpoint,
        headers={
            'Authorization': 'Bearer ' + token['access_token']
            }
        ).json()
    running_status = ""
    statuses = api_result['statuses']
    for status in statuses:
        if 'PowerState' in status['code']:
            running_status = status['displayStatus']

    return f"Status of {vm_name}: {running_status}"



if __name__ == "__main__":
    app.run(debug=True, host="localhost")


