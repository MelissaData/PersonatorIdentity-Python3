#!/bin/bash

# Runs the Melissa Personator Identity Cloud API Python 3 sample.
#
# This script runs PersonatorIdentityPython3.py with python3, passing along the license
# and (if supplied) the action and lookup fields.
#
# Overall flow:
#   1. Parse the command-line options below.
#   2. Resolve the license (--license, then a prompt, then the MD_LICENSE environment variable).
#   3. Run PersonatorIdentityPython3.py: with the action/lookup fields if any was supplied,
#      otherwise with only the license (the Python program prompts for each field).
#
# Options (each takes a value):
#   --action               Action to request: check, verify or screen.
#   --fullname             Full name to test.
#   --addressline1         Street address to test.
#   --locality             Locality (city) to test.
#   --administrativearea   Administrative area (state/province) to test.
#   --postal               Postal code to test.
#   --country              Country to test.
#   --license              License string. If omitted, the script prompts for it; if the prompt
#                          is left blank, it falls back to MD_LICENSE. Running without --license
#                          always prompts, even when MD_LICENSE is set.
#
# PersonatorIdentityPython3.py is found relative to the current directory, so run the script from its own folder.
#
# Examples:
#   ./PersonatorIdentityPython3.sh --license "your-license"
#   ./PersonatorIdentityPython3.sh --action "check" --fullname "Raymond Melissa" --addressline1 "22382 Avenida Empresa" --locality "Rancho Santa Margarita" --administrativearea "CA" --postal "92688" --country "United States" --license "your-license"

######################### Constants ##########################

RED='\033[0;31m' #RED
NC='\033[0m' # No Color

######################### Parameters ##########################

action=""
fullname=""
addressline1=""
locality=""
administrativearea=""
postal=""
country=""
license=""

# Read each --flag and its value. A flag with no value, or whose value starts with
# "-", is an error. Unrecognized options are ignored.
while [ $# -gt 0 ] ; do
  case $1 in
    --action) 
        if [ -z "$2" ] || [[ $2 == -* ]];
        then
            printf "${RED}Error: Missing an argument for parameter \'action\'.${NC}\n"  
            exit 1
        fi 

        action="$2"
        shift
        ;;
    --fullname) 
        if [ -z "$2" ] || [[ $2 == -* ]];
        then
            printf "${RED}Error: Missing an argument for parameter \'fullname\'.${NC}\n"  
            exit 1
        fi 

        fullname="$2"
        shift
        ;;
    --addressline1)  
        if [ -z "$2" ] || [[ $2 == -* ]];
        then
            printf "${RED}Error: Missing an argument for parameter \'addressline1\'.${NC}\n"  
            exit 1
        fi 

        addressline1="$2"
        shift
        ;;
    --locality) 
        if [ -z "$2" ] || [[ $2 == -* ]];
        then
            printf "${RED}Error: Missing an argument for parameter \'locality\'.${NC}\n"  
            exit 1
        fi 

        locality="$2"
        shift
        ;;
    --administrativearea)         
        if [ -z "$2" ] || [[ $2 == -* ]];
        then
            printf "${RED}Error: Missing an argument for parameter \'administrativearea\'.${NC}\n"  
            exit 1
        fi 
        
        administrativearea="$2"
        shift
        ;;
    --postal) 
        if [ -z "$2" ] || [[ $2 == -* ]];
        then
            printf "${RED}Error: Missing an argument for parameter \'postal\'.${NC}\n"  
            exit 1
        fi 

        postal="$2"
        shift
        ;;
    --country) 
        if [ -z "$2" ] || [[ $2 == -* ]];
        then
            printf "${RED}Error: Missing an argument for parameter \'country\'.${NC}\n"  
            exit 1
        fi 

        country="$2"
        shift
        ;;
    --license) 
        if [ -z "$2" ] || [[ $2 == -* ]];
        then
            printf "${RED}Error: Missing an argument for parameter \'license\'.${NC}\n"  
            exit 1
        fi 

        license="$2"
        shift 
        ;;
  esac
  shift
done

########################## Main ############################
printf "\n==================== Melissa Personator Identity Cloud API =====================\n"

# Get license (either from parameters or user input)
if [ -z "$license" ];
then
  printf "Please enter your license string: "
  read license
fi

# Check for License from Environment Variables 
if [ -z "$license" ];
then
  license=`echo $MD_LICENSE` 
fi

if [ -z "$license" ];
then
  printf "\nLicense String is invalid!\n"
  exit 1
fi

# Run project
# No action/lookup fields supplied -> run with only the license (the program prompts);
# otherwise pass all of them through. Unsupplied fields arrive as empty strings and the
# program prompts for them.
if [ -z "$action" ] && [ -z "$fullname" ] && [ -z "$addressline1" ] && [ -z "$locality" ] && [ -z "$administrativearea" ] && [ -z "$postal" ] && [ -z "$country" ];
then
    python3 PersonatorIdentityPython3.py --license "$license"
else
    python3 PersonatorIdentityPython3.py \
		--license "$license" \
		--action "$action" \
		--fullname "$fullname" \
		--addressline1 "$addressline1" \
		--locality "$locality" \
		--administrativearea "$administrativearea" \
		--postal "$postal" \
		--country "$country"
fi

