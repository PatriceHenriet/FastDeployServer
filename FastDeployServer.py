#
# GetSystemHWInventoryREDFISH. Python script using Redfish API to get system hardware inventory
#
# _author_ = Texas Roemer <Texas_Roemer@Dell.com>
# _version_ = 7.0
#
# Copyright (c) 2018, Dell, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#


import requests, json, sys, re, time, warnings, argparse, os

from datetime import datetime

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(
    description="Python script using Redfish API to get system hardware inventory(output will be printed to the screen and also copied to a text file). This includes information for storage controllers, memory, network devices, general system details, power supplies, hard drives, fans, backplanes, processors")
parser.add_argument('-ip', help='iDRAC IP address', required=True)
parser.add_argument('-u', help='iDRAC username', required=True)
parser.add_argument('-p', help='iDRAC password', required=True)
parser.add_argument('script_examples', action="store_true",
                    help='GetSystemHWInventoryREDFISH.py -ip 192.168.0.120 -u root -p calvin -m y, this example will get only memory information. GetSystemHWInventoryREDFISH.py -ip 192.168.0.120 -u root -p calvin -c y -m y, this example will get only processor and memory information. GetSystemHWInventoryREDFISH.py -ip 192.168.0.120 -u root -p calvin -a y, this example will get all system information: general system information, processor, memory, fans, power supplies, hard drives, storage controllers, network devices')
parser.add_argument('-s', help='Get system information only, pass in \"y\"', required=False)
parser.add_argument('-m', help='Get memory information only, pass in \"y\"', required=False)
parser.add_argument('-c', help='Get processor information only, pass in \"y\"', required=False)
parser.add_argument('-f', help='Get fan information only, pass in \"y\"', required=False)
parser.add_argument('-ps', help='Get power supply information only, pass in \"y\"', required=False)
parser.add_argument('-S', help='Get storage information only, pass in \"y\"', required=False)
parser.add_argument('-n', help='Get network device information only, pass in \"y\"', required=False)
parser.add_argument('-a', help='Get all system information / device information, pass in \"y\"', required=False)

args = vars(parser.parse_args())

idrac_ip = args["ip"]
idrac_username = args["u"]
idrac_password = args["p"]


def check_supported_idrac_version():
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1' % idrac_ip, verify=False,
                            auth=(idrac_username, idrac_password))
    data = response.json()
    if response.status_code != 200:
        print("\n- WARNING, iDRAC version installed does not support this feature using Redfish API")
        sys.exit()
    else:
        pass


def get_system_information():
    f = open("hw_inventory.txt", "a")
    response = requests.get('https://%s/redfish/v1/Systems/System.Embedded.1' % idrac_ip, verify=False,
                            auth=(idrac_username, idrac_password))
    data = response.json()
    if response.status_code != 200:
        print("\n- FAIL, get command failed, error is: %s" % data)
        sys.exit()
    else:
        message = "\n---- System Information ----\n"
        f.writelines(message)
        f.writelines("\n")
        print(message)
    for i in data.items():
        if i[0] == '@odata.id' or i[0] == '@odata.context' or i[0] == 'Links' or i[0] == 'Actions' or i[
            0] == '@odata.type' or i[0] == 'Description' or i[0] == 'EthernetInterfaces' or i[0] == 'Storage' or i[
            0] == 'Processors' or i[0] == 'Memory' or i[0] == 'SecureBoot' or i[0] == 'NetworkInterfaces' or i[
            0] == 'Bios' or i[0] == 'SimpleStorage' or i[0] == 'PCIeDevices' or i[0] == 'PCIeFunctions':
            pass
        elif i[0] == 'Oem':
            for ii in i[1]['Dell']['DellSystem'].items():
                if ii[0] == '@odata.context' or ii[0] == '@odata.type':
                    pass
                else:
                    message = "%s: %s" % (ii[0], ii[1])
                    f.writelines(message)
                    f.writelines("\n")
                    print(message)


        elif i[0] == 'Boot':
            try:
                message = "BiosBootMode: %s" % i[1]['BootSourceOverrideMode']
                f.writelines(message)
                f.writelines("\n")
                print(message)
            except:
                pass
        else:
            message = "%s: %s" % (i[0], i[1])
            f.writelines(message)
            f.writelines("\n")
            print(message)
    f.close()



if __name__ == "__main__":
    check_supported_idrac_version()
    if args["s"]:
        get_system_information()
    print("\n- WARNING, output also captured in \"%s\hw_inventory.txt\" file" % os.getcwd())
