import requests
from time import sleep


class SFC:
    def __init__(self, odl_addr, odl_port):
        self.odl_addr = odl_addr
        self.odl_port = odl_port

    def _create_sf(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + "/restconf/config/service-function:service-functions/"

        payload = "{\r\n  \"service-functions\": {\r\n    \"service-function\": [\r\n      {\r\n        \"name\": \"SF2\",\r\n        \"rest-uri\": \"http://127.0.0.1:5000\",\r\n        \"sf-data-plane-locator\": [\r\n          {\r\n            \"name\": \"vxlan\",\r\n            \"port\": 10001,\r\n            \"ip\": \"127.0.0.1\",\r\n            \"service-function-forwarder\": \"SFF1\",\r\n            \"transport\": \"service-locator:vxlan-gpe\"\r\n          }\r\n        ],\r\n        \"type\": \"dpi\",\r\n        \"ip-mgmt-address\": \"127.0.0.1\"\r\n      },\r\n      {\r\n        \"name\": \"SF1\",\r\n        \"rest-uri\": \"http://127.0.0.1:5000\",\r\n        \"sf-data-plane-locator\": [\r\n          {\r\n            \"name\": \"vxlan\",\r\n            \"port\": 10000,\r\n            \"ip\": \"127.0.0.1\",\r\n            \"service-function-forwarder\": \"SFF1\",\r\n            \"transport\": \"service-locator:vxlan-gpe\"\r\n          }\r\n        ],\r\n        \"type\": \"firewall\",\r\n        \"ip-mgmt-address\": \"127.0.0.1\"\r\n      }\r\n    ]\r\n  }\r\n}"
        headers = {
            'Cache-Control': 'no-cache',
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def _create_node(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + "/restconf/config/service-node:service-nodes"

        payload = "{\r\n  \"service-nodes\": {\r\n    \"service-node\": [\r\n      {\r\n        \"name\": \"Node2\",\r\n        \"service-function\": [\r\n          \"SF2\"\r\n        ],\r\n        \"ip-mgmt-address\": \"127.0.0.1\",\r\n        \"service-function-forwarder\": [\r\n          \"SFF1\"\r\n        ]\r\n      },\r\n      {\r\n        \"name\": \"Node1\",\r\n        \"service-function\": [\r\n          \"SF1\"\r\n        ],\r\n        \"ip-mgmt-address\": \"127.0.0.1\",\r\n        \"service-function-forwarder\": [\r\n          \"SFF1\"\r\n        ]\r\n      }\r\n    ]\r\n  }\r\n};"
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def _create_sff(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + "/restconf/config/service-function-forwarder:service-function-forwarders/"

        payload = "{\r\n  \"service-function-forwarders\": {\r\n    \"service-function-forwarder\": [\r\n      {\r\n        \"name\": \"SFF1\",\r\n        \"service-node\": \"Node1\",\r\n        \"sff-data-plane-locator\": [\r\n          {\r\n            \"name\": \"dp1\",\r\n            \"data-plane-locator\": {\r\n              \"port\": 4789,\r\n              \"ip\": \"127.0.0.1\",\r\n              \"transport\": \"service-locator:vxlan-gpe\"\r\n            },\r\n            \"service-function-forwarder-ovs:ovs-options\": {}\r\n          }\r\n        ],\r\n        \"service-function-forwarder-ovs:ovs-bridge\": {},\r\n        \"rest-uri\": \"http://127.0.0.1:5000\",\r\n        \"service-function-dictionary\": [\r\n          {\r\n            \"name\": \"SF1\",\r\n            \"sff-sf-data-plane-locator\": {\r\n              \"sf-dpl-name\": \"vxlan\",\r\n              \"sff-dpl-name\": \"dp1\"\r\n            },\r\n            \"failmode\": \"service-function-forwarder:open\"\r\n          },\r\n          {\r\n            \"name\": \"SF2\",\r\n            \"sff-sf-data-plane-locator\": {\r\n              \"sf-dpl-name\": \"vxlan\",\r\n              \"sff-dpl-name\": \"dp1\"\r\n            },\r\n            \"failmode\": \"service-function-forwarder:open\"\r\n          }\r\n        ],\r\n        \"ip-mgmt-address\": \"127.0.0.1\"\r\n      }\r\n    ]\r\n  }\r\n}\r\n"
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def _create_sfc(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + "/restconf/config/service-function-chain:service-function-chains/"

        payload = "{\r\n  \"service-function-chains\": {\r\n    \"service-function-chain\": [\r\n      {\r\n        \"name\": \"sfc-chain1\",\r\n        \"sfc-service-function\": [\r\n          {\r\n            \"name\": \"sf-chain-node-1\",\r\n            \"type\": \"dpi\"\r\n          },\r\n          {\r\n            \"name\": \"sf-chain-node-2\",\r\n            \"type\": \"firewall\"\r\n          }\r\n        ]\r\n      }\r\n    ]\r\n  }\r\n}"
        headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def _create_sfp(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + "/restconf/config/service-function-path:service-function-paths/"

        payload = "{\r\n  \"service-function-paths\": {\r\n    \"service-function-path\": [\r\n      {\r\n        \"name\": \"sfc-path1\",\r\n        \"service-chain-name\": \"sfc-chain1\",\r\n        \"transport-type\": \"service-locator:vxlan-gpe\",\r\n        \"symmetric\": true\r\n      }\r\n    ]\r\n  }\r\n}"
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1wksfeupuzf5v1svvyfijiqsgk'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

    def _get_rendered_sfp(self):
        url = "http://" + self.odl_addr + ":" + self.odl_port + "/restconf/operational/rendered-service-path:rendered-service-paths/"

        payload = {}
        headers = {
            'Authorization': 'Basic YWRtaW46YWRtaW4=',
            'Cookie': 'JSESSIONID=9dbvuhluh4rh13pqa1rusz3av'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text.encode('utf8'))

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
    sfc_connection.apply_config()

