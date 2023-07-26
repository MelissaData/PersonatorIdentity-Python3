# Name:    PersonatorIdentityCloudAPI
# Purpose: Execute the PersonatorIdentityCloudAPI program

######################### Parameters ##########################
param(
    $action = '', 
    $fullname = '',
    $addressline1 = '', 
    $locality = '', 
    $administrativearea = '', 
    $postal = '', 
    $country = '', 
    $license = '', 
    [switch]$quiet = $false
    )

########################## Main ############################
Write-Host "`n==================== Melissa Personator Identity Cloud API =====================`n"

# Get license (either from parameters or user input)
if ([string]::IsNullOrEmpty($license) ) {
  $license = Read-Host "Please enter your license string"
}

# Check for License from Environment Variables 
if ([string]::IsNullOrEmpty($license) ) {
  $license = $env:MD_LICENSE 
}

if ([string]::IsNullOrEmpty($license)) {
  Write-Host "`nLicense String is invalid!"
  Exit
}

# Run project
if ([string]::IsNullOrEmpty($action) -and [string]::IsNullOrEmpty($fullname) -and [string]::IsNullOrEmpty($addressline1) -and [string]::IsNullOrEmpty($locality) -and [string]::IsNullOrEmpty($administrativearea) -and [string]::IsNullOrEmpty($postal) -and [string]::IsNullOrEmpty($country)) {
  python3 PersonatorIdentityPython3.py --license $license 
}
else {
  python3 PersonatorIdentityPython3.py --license $license --action $action --fullname $fullname --addressline1 $addressline1 --locality $locality --administrativearea $administrativearea --postal $postal --country $country
}
