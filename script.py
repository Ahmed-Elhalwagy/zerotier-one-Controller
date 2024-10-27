import requests
import json
from dotenv import load_dotenv
import os
from tabulate import tabulate
import textwrap
from prompt_toolkit import prompt
from datetime import datetime

load_dotenv()

network_id = ""
node_id = ""

def convert_to_time(timestamp):
    timestamp = timestamp / 1000
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

os.system('clear')

print("WELCOME To Your ZEROTIER-one Controller")
if not os.path.exists(".env"):
    print('Make sure to add your .env file with these keys')
    print('Your API Token with key "ZT_TOKEN"')
    print('Your API URL with key "API_URL"')
    exit(4)
os.system("clear")

print("ZZZZZZZZZZZZZZZZZZZZ          EEEEEEEEEEEEEEEEEEEE         RRRRRRRRRRRRRRRRR            OOOOOOOOOOOOOOOOOO")
print("              ZZZZZ           EEEEEEEEEEEEEEEEEEEE         RRRRRRRRRRRRRRRRRRR         OOOOOOOOOOOOOOOOOOOO")
print("             ZZZZZ            EEE                          RRR         RRRRRRR       OOOOOOOOO      OOOOOOOO")
print("            ZZZZZ             EEE                          RRR         RRRRRRR     OOOOOOOO          OOOOOOO")
print("           ZZZZZ              EEE                          RRR         RRRRRRR     OOOOOOOO            OOOOOOO")
print("          ZZZZZ               EEEEEEEEEEEEEEEE             RRRRRRRRRRRRRRRRRRR     OOOOOOOO            OOOOOOO")
print("         ZZZZZ                EEEEEEEEEEEEEEEE             RRRRRRRRRRRRRRRRRRR     OOOOOOOO            OOOOOOO")
print("        ZZZZZ                 EEE                          RRR   RRRRR             OOOOOOOO            OOOOOOO")
print("       ZZZZZ                  EEE                          RRR    RRRRR            OOOOOOOO            OOOOOOO")
print("      ZZZZZ                   EEE                          RRR     RRRRR           OOOOOOOO            OOOOOOO")
print("     ZZZZZ                    EEEEEEEEEEEEEEEEEEEE         RRR      RRRRR           OOOOOOOO          OOOOOOOO")
print("ZZZZZZZZZZZZZZZZZZZZ          EEEEEEEEEEEEEEEEEEEE         RRR       RRRRR            OOOOOOOOO      OOOOOOOOO")
print("ZZZZZZZZZZZZZZZZZZZZ          EEEEEEEEEEEEEEEEEEEE         RRR        RRRRR             OOOOOOOOOOOOOOOOOOOOOO")
print("ZZZZZZZZZZZZZZZZZZZZ          EEEEEEEEEEEEEEEEEEEE         RRR         RRRRR              OOOOOOOOOOOOOOOOOOO")

while True:
    zt_token = os.getenv('ZT_TOKEN')
    api_url_raw = os.getenv('API_URL')
    api_url = ""

    headers = {
        "X-ZT1-AUTH": f"{zt_token}",
        "Content-Type": "application/json"
    }

    print ('''
    1- List current networks
    2- Create new Network
    3- Get Network info
    4- List network members
    5- Get Member info
    6- Authorize a member
    7- Deauthorize member
    8- Delete a Network member
    9- Delete Network
    10- Status (account tied up with the API token)
    11- Get Random 32 char Token
    12- Add API Token
    13- Delete API Token
    14- quit
    ''')
    option = input("Chose your number: ")

    if option == '1':
        api_url = f"{api_url_raw}/controller/network"
        os.system("clear")
        print ("Listing Current Networks")

        networks = []
        response = requests.get(url=api_url, headers=headers)

        if(response.status_code == 200):
            for net in response.json():
                print(net)
                api_url_network= f"{api_url_raw}/controller/network/{net}"
                response = requests.get(url=api_url_network, headers=headers)
                net_data = response.json()
                network = {
                    "network_id": net_data['nwid'],
                    "network_name": net_data['name'],
                    "ipAssignmentPools": net_data['ipAssignmentPools'],
                    "routes": net_data['routes'],
                    "DNS": net_data['dns'],
                    "Created at": convert_to_time(net_data['creationTime'])
                    }
                networks.append(network)
            if len(networks) == 0:
                print("!!!!! No Netowks to Display !!!!!")
            else:
                print(tabulate(networks, headers="keys", tablefmt="grid"))
                if(len(networks) == 1):
                    network_id = networks[0]["network_id"]
        else:
            print(f"Error {response.text} {response.status_code}")

    elif option == '2':
        os.system('clear')
        print("Create new Network")
        network_name = input("Network Name: ")
        ip_start = input("Ip Range start (e.g., 10.0.0.1): ")
        ip_end = input("Ip Range End (e.g., 10.0.0.254): ")
        subnet = input("Subnet(e.g., 10.0.0.0/24): ")
        api_url= f"{api_url_raw}/controller/network"
        req_body = {
                        "name": network_name,
                        "private": True,
                        "mtu": 2800,
                        "ipAssignmentPools":
                         [ {
                            "ipRangeStart": ip_start,
                            "ipRangeEnd": ip_end
                        }
                         ],
                        "routes": [
                            {
                                "target": subnet,
                                "via" : None
                            }
                        ] ,
                        "ssossoEnabled" : False,
                        "capabilities": ["route", "dns"],
                        "enableBroadcast": True,
                        "v4AssignMode": {
                                "zt": True
                        }
        }

        response = requests.post(url=api_url, headers=headers,data=json.dumps(req_body))
        if(response.status_code == 200):
            os.system("clear")
            print(f"################ Network created successfully: {response.json()['id']} ################")
        else:
            print(f"Failed to create network: {response.status_code} - {response.text}")

    elif option == "3":
        os.system("clear")
        print ("Get Network info")
        network_id = prompt("Enter network ID: ", default=network_id)
        api_url= f"{api_url_raw}/controller/network/{network_id}"
        response = requests.get(url=api_url, headers=headers)
        if(response.status_code == 200):
            data = response.json()
            print(json.dumps(data, indent=4))
        else:
            print(f"Error {response.text} {response.status_code}")

    elif option == "4":
        print("List network members")
        network_id = prompt("Enter network ID: ", default=network_id)
        api_url= f"{api_url_raw}/controller/network/{network_id}/member"

        response = requests.get(url=api_url, headers=headers)
        if(response.status_code == 200):
            members = response.json()
            members_enriched = []

            for m in members:
                api_url_member = f"{api_url_raw}/controller/network/{network_id}/member/{m}"
                response = requests.get(url=api_url_member, headers=headers)
                m_data = response.json()
                member_enriched = {
                    "nodeId": m,
                    "ipAssignments": m_data['ipAssignments',],
                    "Authorized": m_data["authorized"],
                    "creationTime": convert_to_time(m_data['creationTime']),
                    "lastAuthorizedTime": convert_to_time(m_data['lastAuthorizedTime']),
                    } 
                members_enriched.append(member_enriched)
            print(tabulate(members_enriched, headers="keys", tablefmt="grid"))
        else:
            print(f"Error {response.text} {response.status_code}")
    elif option == "5":
        print ("Get Network Member info")
        network_id = prompt("Enter network ID: ", default=network_id)
        node_id = prompt("Enter Member ID (Node ID): ", default=node_id)
        api_url= f"{api_url_raw}/controller/network/{network_id}/member/{node_id}"
        response = requests.get(url=api_url, headers=headers)
        if(response.status_code == 200):
            data = response.json()
            print(json.dumps(data, indent=4))
        else:
            print(f"Error {response.text} {response.status_code}")


    elif option == "6":
        print("Authorize a network member")
        network_id = prompt("Enter network ID: ", default=network_id)
        node_id = prompt("Enter Node ID (Node ID): ", default=node_id)
        api_url= f"{api_url_raw}/controller/network/{network_id}/member/{node_id}"
        req_body = {
              "config": {
              "authorized": True
            }
        }
        response = requests.post(url=api_url, headers=headers,data=json.dumps(req_body))
        if(response.status_code == 200):
            print(f"################ The node {node_id} has been Authorized Successfuly ################")
        else:
            print(f"Failed to Authorize {node_id}")
            print(f"{response.status_code} - {response.text}")

    elif option == "7":
        print("Deauthorize network member")
        network_id = prompt("Enter network ID: ", default=network_id)
        node_id = prompt("Enter Member ID (Node ID): ", default=node_id)
        api_url= f"{api_url_raw}/controller/network/{network_id}/member/{node_id}"
        req_body = {
              "authorized": False
        }
        response = requests.post(url=api_url, headers=headers,data=json.dumps(req_body))
        if(response.status_code == 200):
            print(f"################ The node {node_id} has been Deauthorize Successfuly ################")
        else:
            print(f"Failed to Authorize {node_id}")
            print(f"{response.status_code} - {response.text}")


    elif option == "8":
        print ("Delete A Network Member")
        network_id = prompt("Enter network ID: ", default=network_id)
        node_id = prompt("Enter Member ID (Node ID): ", default=node_id)
        api_url= f"{api_url_raw}/controller/network/{network_id}/member/{node_id}"
        response = requests.delete(url=api_url, headers=headers)
        if(response.status_code == 200):
            print(f"################ The Member {node_id} has been deleted from {network_id} ################")
        else:
            print(f"Error {response.text} {response.status_code}")

    elif option == "9":
        print ("Delete Network")
        network_id = input("Enter network ID: ")
        api_url= f"{api_url_raw}/controller/network/{network_id}"
        response = requests.delete(url=api_url, headers=headers)
        if(response.status_code == 200):
            print(f"################ The Netowrk {network_id} has been deleted Sucessfully ################")
        else:
            print(f"Error {response.text} {response.status_code}")

    elif option == "10":
        print("################ STATUS ################")
        api_url= f"{api_url_raw}/status"
        response = requests.get(url=api_url, headers=headers)
        if(response.status_code == 200):
            data = response.json()
            print(json.dumps(data, indent=4))
        else:
            print(f"Error {response.text} {response.status_code}")

    elif option == "11":
        print("################ TOKEN ################")
        api_url= f"{api_url_raw}/randomToken"
        response = requests.get(url=api_url, headers=headers)
        if(response.status_code == 200):
            data = response.json()
            print(f"Token: {data['token']}")
        else:
            print(f"Error {response.text} {response.status_code}")


    elif option == "12":
        print("################ ADD API Token ################")
        random_api_url= f"{api_url_raw}/randomToken"
        response = requests.get(url=random_api_url, headers=headers)
        if(response.status_code == 200):
            data = response.json()
            token = data['token']
            print("Each token you create is associated with your user account, so it will allow the same level of access to manage and query networks that you have")
            user_id = input("Enter User ID: ")
            token_name = input("Enter Token Name: ")

            req_body = {
                "tokenName": token_name,
                "token": token
            }

            api_url= f"{api_url_raw}/user/{user_id}/token"
            response = requests.post(url=api_url, headers=headers, data=json.dumps(req_body))
            if(response.status_code == 200):
                print(f"The Token '{token_name}' Has been created for user {user_id}")
                print(f"Token: {token}")
            else:
                print(f"Error {response.text} {response.status_code}")
        else:
            print(f"Error {response.text} {response.status_code}")

    elif option == "13":
        print("################ DELETE API TOKEN ################")
        user_id = input("Enter User ID: ")
        token_name = input("Enter Token Name: ")
        api_url= f"{api_url_raw}/user/{user_id}/token/{token_name}"
        response = requests.delete(url=api_url, headers=headers)
        if(response.status_code == 200):
                print(f"Token {token_name} was Deleted Successfuly")
        else:
            print(f"Error {response.text} {response.status_code}")

    elif option == '14':
        print("GoodBye")
        exit(0)
