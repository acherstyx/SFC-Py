import requests
from time import sleep
import json


class SFC:
    def __init__(self, odl_addr, odl_port):
        self.odl_addr = odl_addr
        self.odl_port = odl_port

        self.sf_json = {}
        self.__init_sf_json()
        self.service_node_json = {}
        self.__init_service_node_json()
        self.sff_json = {}
        self.__init_sff_json()
        self.sfc_json = {}
        self.__init_sfc_json()
        self.sfp_json = {}

    def _create_sf(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function:service-functions/"

        payload = "{\r\n  \"service-functions\": {\r\n    \"service-function\": [\r\n      {\r\n        \"name\": \"SF2\",\r\n        \"rest-uri\": \"http://127.0.0.1:5000\",\r\n        \"sf-data-plane-locator\": [\r\n          {\r\n            \"name\": \"vxlan\",\r\n            \"port\": 10001,\r\n            \"ip\": \"127.0.0.1\",\r\n            \"service-function-forwarder\": \"SFF1\",\r\n            \"transport\": \"service-locator:vxlan-gpe\"\r\n          }\r\n        ],\r\n        \"type\": \"dpi\",\r\n        \"ip-mgmt-address\": \"127.0.0.1\"\r\n      },\r\n      {\r\n        \"name\": \"SF1\",\r\n        \"rest-uri\": \"http://127.0.0.1:5000\",\r\n        \"sf-data-plane-locator\": [\r\n          {\r\n            \"name\": \"vxlan\",\r\n            \"port\": 10000,\r\n            \"ip\": \"127.0.0.1\",\r\n            \"service-function-forwarder\": \"SFF1\",\r\n            \"transport\": \"service-locator:vxlan-gpe\"\r\n          }\r\n        ],\r\n        \"type\": \"firewall\",\r\n        \"ip-mgmt-address\": \"127.0.0.1\"\r\n      }\r\n    ]\r\n  }\r\n}"
        headers = {
            'Cache-Control': 'no-cache',
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("[Create SF]", response.status_code, response.text.encode('utf8'))

    def _create_node(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-node:service-nodes"

        payload = "{\r\n  \"service-nodes\": {\r\n    \"service-node\": [\r\n      {\r\n        \"name\": \"Node2\",\r\n        \"service-function\": [\r\n          \"SF2\"\r\n        ],\r\n        \"ip-mgmt-address\": \"127.0.0.1\",\r\n        \"service-function-forwarder\": [\r\n          \"SFF1\"\r\n        ]\r\n      },\r\n      {\r\n        \"name\": \"Node1\",\r\n        \"service-function\": [\r\n          \"SF1\"\r\n        ],\r\n        \"ip-mgmt-address\": \"127.0.0.1\",\r\n        \"service-function-forwarder\": [\r\n          \"SFF1\"\r\n        ]\r\n      }\r\n    ]\r\n  }\r\n};"
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("[Create Node]", response.status_code, response.text.encode('utf8'))

    def _create_sff(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function-forwarder:service-function-forwarders/"

        payload = "{\r\n  \"service-function-forwarders\": {\r\n    \"service-function-forwarder\": [\r\n      {\r\n        \"name\": \"SFF1\",\r\n        \"service-node\": \"Node1\",\r\n        \"sff-data-plane-locator\": [\r\n          {\r\n            \"name\": \"dp1\",\r\n            \"data-plane-locator\": {\r\n              \"port\": 4789,\r\n              \"ip\": \"127.0.0.1\",\r\n              \"transport\": \"service-locator:vxlan-gpe\"\r\n            },\r\n            \"service-function-forwarder-ovs:ovs-options\": {}\r\n          }\r\n        ],\r\n        \"service-function-forwarder-ovs:ovs-bridge\": {},\r\n        \"rest-uri\": \"http://127.0.0.1:5000\",\r\n        \"service-function-dictionary\": [\r\n          {\r\n            \"name\": \"SF1\",\r\n            \"sff-sf-data-plane-locator\": {\r\n              \"sf-dpl-name\": \"vxlan\",\r\n              \"sff-dpl-name\": \"dp1\"\r\n            },\r\n            \"failmode\": \"service-function-forwarder:open\"\r\n          },\r\n          {\r\n            \"name\": \"SF2\",\r\n            \"sff-sf-data-plane-locator\": {\r\n              \"sf-dpl-name\": \"vxlan\",\r\n              \"sff-dpl-name\": \"dp1\"\r\n            },\r\n            \"failmode\": \"service-function-forwarder:open\"\r\n          }\r\n        ],\r\n        \"ip-mgmt-address\": \"127.0.0.1\"\r\n      }\r\n    ]\r\n  }\r\n}\r\n"
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("[Create SFF]", response.status_code, response.text.encode('utf8'))

    def _create_sfc(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function-chain:service-function-chains/"

        payload = "{\r\n  \"service-function-chains\": {\r\n    \"service-function-chain\": [\r\n      {\r\n        \"name\": \"sfc-chain1\",\r\n        \"sfc-service-function\": [\r\n          {\r\n            \"name\": \"sf-chain-node-1\",\r\n            \"type\": \"dpi\"\r\n          },\r\n          {\r\n            \"name\": \"sf-chain-node-2\",\r\n            \"type\": \"firewall\"\r\n          }\r\n        ]\r\n      }\r\n    ]\r\n  }\r\n}"
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("[Create SFC]", response.status_code, response.text.encode('utf8'))

    def _create_sfp(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/config/service-function-path:service-function-paths/"

        payload = "{\r\n  \"service-function-paths\": {\r\n    \"service-function-path\": [\r\n      {\r\n        \"name\": \"sfc-path1\",\r\n        \"service-chain-name\": \"sfc-chain1\",\r\n        \"transport-type\": \"service-locator:vxlan-gpe\",\r\n        \"symmetric\": true\r\n      }\r\n    ]\r\n  }\r\n}"
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        print("[Create SFP]", response.status_code, response.text.encode('utf8'))

    def _get_rendered_sfp(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + \
              "/restconf/operational/rendered-service-path:rendered-service-paths/"

        payload = {}
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=9dbvuhluh4rh13pqa1rusz3av'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text.encode('utf8'))

    def __init_sf_json(self):
        self.sf_json["service-functions"] = {}
        self.sf_json["service-functions"]["service-function"] = []

    def add_sf(self, sf_name, ip, port, service_type, sff_name):
        self.sf_json["service-functions"]["service-function"].append({})
        self.sf_json["service-functions"]["service-function"][-1]["name"] = sf_name
        self.sf_json["service-functions"]["service-function"][-1]["rest-uri"] = "http://" + ip + ":5000"
        self.sf_json["service-functions"]["service-function"][-1]["type"] = service_type
        self.sf_json["service-functions"]["service-function"][-1]["ip-mgmt-address"] = ip

        self.sf_json["service-functions"]["service-function"][-1]["sf-data-plane-locator"] = []
        self.sf_json["service-functions"]["service-function"][-1]["sf-data-plane-locator"].append({})
        self.sf_json["service-functions"]["service-function"][-1]["sf-data-plane-locator"][-1]["name"] = "vxlan"
        self.sf_json["service-functions"]["service-function"][-1]["sf-data-plane-locator"][-1]["port"] = port
        self.sf_json["service-functions"]["service-function"][-1]["sf-data-plane-locator"][-1]["ip"] = ip
        self.sf_json["service-functions"]["service-function"][-1]["sf-data-plane-locator"][-1][
            "service-function-forwarder"] = sff_name
        self.sf_json["service-functions"]["service-function"][-1]["sf-data-plane-locator"][-1][
            "transport"] = "service-locator:vxlan-gpe"

        print(json.dumps(self.sf_json))

    def __init_service_node_json(self):
        self.service_node_json["service-nodes"] = {}
        self.service_node_json["service-nodes"]["service-node"] = []

    def add_service_node(self, node_name, sf_name, sff_name, ip):
        self.service_node_json["service-nodes"]["service-node"].append({})
        self.service_node_json["service-nodes"]["service-node"][-1]["name"] = node_name
        self.service_node_json["service-nodes"]["service-node"][-1]["ip-mgmt-address"] = ip
        self.service_node_json["service-nodes"]["service-node"][-1]["service-function"] = [sf_name]
        self.service_node_json["service-nodes"]["service-node"][-1]["service-function-forwarder"] = [sff_name]

        print(json.dumps(self.service_node_json))

    def __init_sff_json(self):
        self.sff_json["service-function-forwarders"] = {}
        self.sff_json["service-function-forwarders"]["service-function-forwarder"] = []

    def add_sff(self, sff_name, node_name, ip, sff_port):
        self.sff_json["service-function-forwarders"]["service-function-forwarder"].append({})
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]["name"] = sff_name
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]["service-node"] = node_name
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1][
            "rest-uri"] = "http://" + ip + ":5000"
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]["ip-mgmt-address"] = ip
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]["sff-data-plane-locator"] = []
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]["sff-data-plane-locator"].append(
            {})
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]["sff-data-plane-locator"][-1][
            "name"] = "dp1"
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]["sff-data-plane-locator"][-1][
            "data-plane-locator"] = {}
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]["sff-data-plane-locator"][-1][
            "data-plane-locator"]["port"] = sff_port
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]["sff-data-plane-locator"][-1][
            "data-plane-locator"]["ip"] = ip
        self.sff_json["service-function-forwarders"]["service-function-forwarder"][-1]["sff-data-plane-locator"][-1][
            "data-plane-locator"]["transport"] = "service-locator:vxlan-gpe"

        print(json.dumps(self.sff_json))

    def __init_sfc_json(self):
        self.sfc_json["service-function-chains"] = {}
        self.sfc_json["service-function-chains"]["service-function-chain"] = []

    def add_sfc(self, sfc_name, service_type_list):
        # 添加单个类别的服务到服务链
        self.sfc_json["service-function-chains"]["service-function-chain"].append({})
        self.sfc_json["service-function-chains"]["service-function-chain"][-1]["name"] = sfc_name
        self.sfc_json["service-function-chains"]["service-function-chain"][-1]["sfc-service-function"] = []

        for index, service_type in enumerate(service_type_list):
            self.sfc_json["service-function-chains"]["service-function-chain"][-1]["sfc-service-function"].append({})
            self.sfc_json["service-function-chains"]["service-function-chain"][-1]["sfc-service-function"][-1][
                "name"] = "chain-node-" + str(index + 1)
            self.sfc_json["service-function-chains"]["service-function-chain"][-1]["sfc-service-function"][-1][
                "type"] = service_type

        print(json.dumps(self.sfc_json))

    def apply_config(self):
        self._create_sf()
        sleep(1)
        self._create_node()
        sleep(1)
        self._create_sff()
        sleep(1)
        self._create_sfc()
        sleep(1)
        self._create_sfp()
        sleep(10)
        self._get_rendered_sfp()


if __name__ == "__main__":
    sfc_connection = SFC("localhost", "8181")
    # sfc_connection.apply_config()
    sfc_connection.add_sf("SF1", "127.0.0.1", "10001", "firewall", "SFF1")
    sfc_connection.add_service_node("Node1", "SF1", "SFF1", "127.0.0.1")
    sfc_connection.add_sff("SFF1", "Node1", "127.0.0.1", 4789)
    sfc_connection.add_sfc("chain-1", ["dpi", "firewall"])
