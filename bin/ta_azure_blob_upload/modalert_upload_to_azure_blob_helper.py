
# encoding = utf-8

def upload_to_azure_blob(azure_account_name, azure_account_key, azure_container, splunk_results_file_path, azure_blob_file_name, proxydict):
    
    import os
    from azure.storage.blob import BlockBlobService
    from azure.storage.blob import ContentSettings
    from azure.storage.common.retry import ExponentialRetry
    import datetime

    # Prefix the Blob file name with now time
    now_time = datetime.datetime.utcnow()
    date_string = now_time.strftime('%Y-%m-%dT%H%M%SZ_')
    azure_blob_file_name = date_string + azure_blob_file_name + '.csv.gz'
    


    # Connecting to the blob service
    block_blob_service = BlockBlobService(account_name=azure_account_name, account_key=azure_account_key)
    block_blob_service.retry = ExponentialRetry(initial_backoff=30, increment_base=2, max_attempts=5).retry
    
    # Use proxy if not empty
    if proxydict:
        proxy_host = str(proxydict['proxy_url'])
        proxy_port = int(proxydict['proxy_port'])
        super(BlockBlobService, block_blob_service).set_proxy(proxy_host, proxy_port)

    full_path_to_file = os.path.join('/opt/splunk/var/run/splunk/dispatch/', splunk_results_file_path)

    # Upload the CSV file
    block_blob_service.create_blob_from_path(azure_container, azure_blob_file_name, full_path_to_file,
        content_settings=ContentSettings(content_type='application/CSV.GZ'))

    return

def process_event(helper, *args, **kwargs):
    """
    # IMPORTANT
    # Do not remove the anchor macro:start and macro:end lines.
    # These lines are used to generate sample code. If they are
    # removed, the sample code will not be updated when configurations
    # are updated.

    [sample_code_macro:start]

    # The following example gets and sets the log level
    helper.set_log_level(helper.log_level)

    # The following example sends rest requests to some endpoint
    # response is a response object in python requests library
    response = helper.send_http_request("http://www.splunk.com", "GET", parameters=None,
                                        payload=None, headers=None, cookies=None, verify=True, cert=None, timeout=None, use_proxy=True)
    # get the response headers
    r_headers = response.headers
    # get the response body as text
    r_text = response.text
    # get response body as json. If the body text is not a json string, raise a ValueError
    r_json = response.json()
    # get response cookies
    r_cookies = response.cookies
    # get redirect history
    historical_responses = response.history
    # get response status code
    r_status = response.status_code
    # check the response status, if the status is not sucessful, raise requests.HTTPError
    response.raise_for_status()


    # The following example gets the alert action parameters and prints them to the log
    azure_blob_file_name = helper.get_param("azure_blob_file_name")
    helper.log_info("azure_blob_file_name={}".format(azure_blob_file_name))

    azure_account_name = helper.get_param("azure_account_name")
    helper.log_info("azure_account_name={}".format(azure_account_name))

    azure_account_key = helper.get_param("azure_account_key")
    helper.log_info("azure_account_key={}".format(azure_account_key))

    azure_container = helper.get_param("azure_container")
    helper.log_info("azure_container={}".format(azure_container))


    # The following example adds two sample events ("hello", "world")
    # and writes them to Splunk
    # NOTE: Call helper.writeevents() only once after all events
    # have been added
    helper.addevent("hello", sourcetype="sample_sourcetype")
    helper.addevent("world", sourcetype="sample_sourcetype")
    helper.writeevents(index="summary", host="localhost", source="localhost")

    # The following example gets the events that trigger the alert
    events = helper.get_events()
    for event in events:
        helper.log_info("event={}".format(event))

    # helper.settings is a dict that includes environment configuration
    # Example usage: helper.settings["server_uri"]
    helper.log_info("server_uri={}".format(helper.settings["server_uri"]))
    [sample_code_macro:end]
    """

    helper.log_info("Alert action upload_to_azure_blob started.")

    # Get search id
    splunk_sid = helper.settings.get("sid")
    splunk_results_file_path = splunk_sid + "/results.csv.gz"
    helper.log_info("splunk_results_file_path={}".format(splunk_results_file_path))

    search_name = helper.settings.get('search_name')

    # Get parameter values

    azure_blob_file_name = helper.get_param("azure_blob_file_name")
    helper.log_info("azure_blob_file_name={}".format(azure_blob_file_name))
    if not azure_blob_file_name.strip():
        azure_blob_file_name = search_name
        helper.log_info("No azure_blob_file_name name given, using search_name instead")

    azure_account_name = helper.get_param("azure_account_name")
    helper.log_info("azure_account_name={}".format(azure_account_name))

    azure_account_key = helper.get_param("azure_account_key")
    helper.log_info("azure_account_key=<removed>")

    azure_container = helper.get_param("azure_container")
    helper.log_info("azure_container={}".format(azure_container))
    
    proxydict = helper.get_proxy()
    helper.log_info("proxysettings={}".format(proxydict))

    helper.log_info("Starting upload_to_azure_blob.")
    upload_to_azure_blob(azure_account_name, azure_account_key, azure_container, splunk_results_file_path, azure_blob_file_name, proxydict)

    helper.log_info("Alert action upload_to_azure_blob finished.")

    return 0
