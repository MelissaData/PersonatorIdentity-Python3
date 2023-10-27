
import json
import requests
import argparse
import urllib.parse

def main():
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

  call_api(base_service_url, service_endpoint, license, action, fullname, addressline1, locality, administrativearea, postal, country)

def get_contents(base_service_url, request_query):
    url = urllib.parse.urljoin(base_service_url, request_query)
    response = requests.get(url)
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
            input_action = action
            input_fullname = fullname
            input_addressline1 = addressline1
            input_locality = locality
            input_administrativearea = administrativearea
            input_postal = postal
            input_country = country

        while not input_action or not input_fullname or not input_addressline1 or not input_locality or not input_administrativearea or not input_postal or not input_country:
            print("\nFill in each value to see results")
            if not input_action:
                input_fullname = input("\nAction: ")
            if not input_fullname:
                input_fullname = input("\nFulll Name: ")
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

        if (action is not None) and (fullname is not None) and (addressline1 is not None) and (locality is not None) and (administrativearea is not None) and (postal is not None) and (country is not None):
            concat = action + fullname + addressline1 + locality + administrativearea + postal + country
        else:
            concat = None

        if concat is not None and concat != "":
            is_valid = True
            should_continue_running = False

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
