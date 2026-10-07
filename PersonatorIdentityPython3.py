"""
Personator Identity verifies a person's contact record worldwide (name and address) and
returns name, address, email, phone and identity information. The requested action
(check, verify or screen) controls what the service does with the record.

High-level flow of this sample:
  1. ARGS    - main reads any --flag values off the command line with argparse.
  2. INPUT   - call_api fills in whatever wasn't supplied via interactive prompts.
  3. REQUEST - call_api builds the REST query string (license + input fields).
  4. CALL    - get_contents issues the GET request and pretty-prints the JSON response.

This sample is a thin HTTP client: it builds a query string, sends a GET request to
the Personator Identity Cloud API, and prints the JSON response.

Reference:
  - Documentation: https://docs.melissa.com/cloud-api/personator-identity/personator-identity-index.html
  - Release notes: https://releasenotes.melissa.com/cloud-api/personator-identity/
  - Result codes:  https://docs.melissa.com/melissa/result-codes/result-codes-index.html
"""

import json
import requests
import argparse
import urllib.parse

def main():
  """
  Entry point. Reads the optional command-line arguments, then hands control to
  call_api, which performs the actual request/response cycle.

  Recognized flags (each followed by its value, e.g. --action "check"):
  --license/-l, --action, --fullname, --addressline1, --locality, --administrativearea,
  --postal, --country.
  Any flag not supplied is None, and call_api prompts for it interactively.
  """
  base_service_url = "https://globalpersonator.melissadata.net/"
  service_endpoint = "v1/doContactVerify"

  # Create an ArgumentParser object
  parser = argparse.ArgumentParser(description='Personator Identity command line arguments parser')

  # Define the command line arguments
  parser.add_argument('--license', '-l', type=str, help='License key')
  parser.add_argument('--action', type=str, help='Action')
  parser.add_argument('--fullname', type=str, help='Full Name')
  parser.add_argument('--addressline1', type=str, help='Address Line 1')
  parser.add_argument('--locality', type=str, help='Locality')
  parser.add_argument('--administrativearea', type=str, help='Administrative Area')
  parser.add_argument('--postal', type=str, help='Postal Code')
  parser.add_argument('--country', type=str, help='Country')

  # Parse the command line arguments
  args = parser.parse_args()

  # Access the values of the command line arguments
  license = args.license
  action = args.action
  fullname = args.fullname
  addressline1 = args.addressline1
  locality = args.locality
  administrativearea = args.administrativearea
  postal = args.postal
  country = args.country

  # Run the lookup with whatever values were passed on the command line.
  call_api(base_service_url, service_endpoint, license, action, fullname, addressline1, locality, administrativearea, postal, country)

def get_contents(base_service_url, request_query):
    """
    Issues the GET request against the Personator Identity endpoint and pretty-prints
    the API call and the JSON response to the console.

    Args:
        base_service_url: The Personator Identity Cloud API base URL.
        request_query: The endpoint path plus query string built by call_api.
    """
    url = urllib.parse.urljoin(base_service_url, request_query)
    response = requests.get(url)

    # Re-serialize with indentation so the raw response is easier to read.
    obj = json.loads(response.text)
    pretty_response = json.dumps(obj, indent=4)

    print("\n==================================== OUTPUT ====================================\n")

    print("API Call: ")
    for i in range(0, len(url), 70):
        if i + 70 < len(url):
            print(url[i:i+70])
        else:
            print(url[i:len(url)])
    print("\nAPI Response:")
    print(pretty_response)

def call_api(base_service_url, service_endpoint, license, action, fullname, addressline1, locality, administrativearea, postal, country):
    """
    Drives the interactive/CLI loop: gathers the required lookup fields, builds and
    submits the REST query, prints the result, and optionally repeats for another record.

    It runs a single pass and exits only when every lookup field (including the action)
    was supplied on the command line. Otherwise it loops, asking for a new record each
    pass until the user answers "N".

    Args:
        base_service_url: The Personator Identity Cloud API base URL.
        service_endpoint: The specific Personator Identity endpoint path to call.
        license: The Melissa license string sent with every request.
        action: The action to request (e.g. check, verify, screen), or None to prompt for it.
        fullname: A full name to test, or None to prompt for it.
        addressline1: A street address to test, or None to prompt for it.
        locality: A locality (city) to test, or None to prompt for it.
        administrativearea: An administrative area (state/province) to test, or None to prompt for it.
        postal: A postal code to test, or None to prompt for it.
        country: A country to test, or None to prompt for it.
    """
    print("\n=============== WELCOME TO MELISSA PERSONATOR IDENTITY CLOUD API ===============\n")

    should_continue_running = True
    while should_continue_running:
        input_action = ""
        input_fullname = ""
        input_addressline1 = ""
        input_locality = ""
        input_administrativearea = ""
        input_postal = ""
        input_country = ""

        # No lookup values (including the action) were supplied via command line, so
        # prompt for every field.
        if not action and not fullname and not addressline1 and not locality and not administrativearea and not postal and not country:
            print("\nFill in each value to see results")
            input_action = input("Action: ")
            input_fullname = input("Full Name: ")
            input_addressline1 = input("Addressline1: ")
            input_locality = input("Locality: ")
            input_administrativearea = input("Administrative Area: ")
            input_postal = input("Postal: ")
            input_country = input("Country: ")
        else:
            # At least one lookup field was supplied via command line; use those values as-is.
            input_action = action
            input_fullname = fullname
            input_addressline1 = addressline1
            input_locality = locality
            input_administrativearea = administrativearea
            input_postal = postal
            input_country = country

        # Prompt individually for any still-missing required field.
        while not input_action or not input_fullname or not input_addressline1 or not input_locality or not input_administrativearea or not input_postal or not input_country:
            print("\nFill in each value to see results")
            if not input_action:
                input_action = input("\nAction: ")
            if not input_fullname:
                input_fullname = input("\nFull Name: ")
            if not input_addressline1:
                input_addressline1 = input("\nAddressline1: ")
            if not input_locality:
                input_locality = input("\nLocality: ")
            if not input_administrativearea:
                input_administrativearea = input("\nAdministrative Area: ")
            if not input_postal:
                input_postal = input("\nPostal: ")
            if not input_country:
                input_country = input("\nCountry: ")

        # Map input fields to the API's expected query parameter names and
        # request a JSON response.
        inputs = {
            "format": "json",
            "act": input_action,
            "full": input_fullname,
            "a1": input_addressline1,
            "loc": input_locality,
            "admarea": input_administrativearea,
            "postal": input_postal,
            "ctry": input_country
        }

        print("\n===================================== INPUTS ===================================\n")
        print(f"\t   Base Service Url: {base_service_url}")
        print(f"\t  Service End Point: {service_endpoint}")
        print(f"\t             Action: {input_action}")
        print(f"\t          Full Name: {input_fullname}")
        print(f"\t       Addressline1: {input_addressline1}")
        print(f"\t           Locality: {input_locality}")
        print(f"\t AdministrativeArea: {input_administrativearea}")
        print(f"\t        Postal Code: {input_postal}")
        print(f"\t            Country: {input_country}")

       # Create Service Call
        # Set the License String in the Request
        rest_request = f"&id={urllib.parse.quote_plus(license)}"

        # Set the Input Parameters
        for k, v in inputs.items():
            rest_request += f"&{k}={urllib.parse.quote_plus(v)}"

        # Build the final REST String Query
        rest_request = service_endpoint + f"?{rest_request}"

        # Submit to the Web Service.
        success = False
        retry_counter = 0

        while not success and retry_counter < 5:
            try: #retry just in case of network failure
                get_contents(base_service_url, rest_request)
                print()
                success = True
            except Exception as ex:
                retry_counter += 1
                print(ex)
                return

        is_valid = False;

        # If every lookup field came from the command line, treat this as a one-shot
        # run rather than looping for additional records.
        if (action is not None) and (fullname is not None) and (addressline1 is not None) and (locality is not None) and (administrativearea is not None) and (postal is not None) and (country is not None):
            concat = action + fullname + addressline1 + locality + administrativearea + postal + country
        else:
            concat = None

        if concat is not None and concat != "":
            is_valid = True
            should_continue_running = False

        # Otherwise ask whether to test another record. Keep prompting until we get a
        # valid Y/N. "N" ends the program; "Y" falls through to another pass.
        while not is_valid:
            test_another_response = input("\nTest another record? (Y/N)")
            if test_another_response != '':
                test_another_response = test_another_response.lower()
                if test_another_response == 'y':
                    is_valid = True
                elif test_another_response == 'n':
                    is_valid = True
                    should_continue_running = False
                else:
                    print("Invalid Response, please respond 'Y' or 'N'")

    print("\n===================== THANK YOU FOR USING MELISSA CLOUD API ====================\n")

main()
