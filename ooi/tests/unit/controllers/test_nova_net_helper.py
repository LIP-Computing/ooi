# -*- coding: utf-8 -*-

# Copyright 2015 LIP - INDIGO-DataCloud
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import uuid

import mock

from ooi.api import helpers
from ooi.tests import base
from ooi.tests import fakes
from ooi.tests import fakes_network
from ooi import utils


class TestNovaNetOpenStackHelper(base.TestCase):
    def setUp(self):
        super(TestNovaNetOpenStackHelper, self).setUp()
        self.version = "version foo bar baz"
        self.helper = helpers.OpenStackHelper(None, self.version)

    @mock.patch.object(helpers.OpenStackHelper, "_get_req")
    @mock.patch.object(helpers.OpenStackHelper, "tenant_from_req")
    def test_list_networks_with_public(self, m_t, m_rq):
        id = uuid.uuid4().hex
        resp = fakes_network.create_fake_json_resp({"networks": [{"id": id}]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        resp_float = fakes_network.create_fake_json_resp(
            {"floating_ip_pools": [{"id": id}]}, 200
        )
        req_mock_float = mock.MagicMock()
        req_mock_float.get_response.return_value = resp_float
        m_rq.side_effect = [req_mock, req_mock_float]
        ret = self.helper.list_networks(None)
        self.assertEqual(2, ret.__len__())

    @mock.patch.object(helpers.OpenStackHelper, "_get_req")
    @mock.patch.object(helpers.OpenStackHelper, "tenant_from_req")
    def test_list_networks_with_no_public(self, m_t, m_rq):
        id = uuid.uuid4().hex
        resp = fakes_network.create_fake_json_resp({"networks": [{"id": id}]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        resp_float = fakes_network.create_fake_json_resp(
            {"floating_ip_pools": []}, 204
        )
        req_mock_float = mock.MagicMock()
        req_mock_float.get_response.return_value = resp_float
        m_rq.side_effect = [req_mock, req_mock_float]
        ret = self.helper.list_networks(None)
        self.assertEqual(1, ret.__len__())

    @mock.patch.object(helpers.OpenStackHelper, "_get_req")
    @mock.patch.object(helpers.OpenStackHelper, "tenant_from_req")
    def test_list_networks(self, m_t, m_rq):
        id = uuid.uuid4().hex
        tenant_id = uuid.uuid4().hex
        m_t.return_value = tenant_id
        resp = fakes_network.create_fake_json_resp({"networks": [{"id": id}]}, 200)
        resp_float = fakes_network.create_fake_json_resp(
            {"floating_ip_pools": [{"id": id}]}, 200
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        req_mock_float = mock.MagicMock()
        req_mock_float.get_response.return_value = resp_float
        m_rq.side_effect = [req_mock, req_mock_float]
        ret = self.helper.list_networks(None)
        self.assertEqual(id, ret[0]['id'])
        self.assertEqual(
            {'method': 'GET',
             'path': '/%s/os-networks' % (tenant_id)},
            m_rq.call_args_list[0][1]
        )
        self.assertEqual(
            {'method': 'GET',
             'path': '/%s/os-floating-ip-pools' % (tenant_id)},
            m_rq.call_args_list[1][1]
        )

    def test_get_network_public(self):
        id = 'PUBLIC'
        ret = self.helper.get_network_details(None, id)
        self.assertEqual(id, ret["id"])

    @mock.patch.object(helpers.OpenStackHelper, "_get_req")
    @mock.patch.object(helpers.OpenStackHelper, "tenant_from_req")
    def test_get_network(self, m_t, m_rq):
        id = uuid.uuid4().hex
        address = uuid.uuid4().hex
        gateway = uuid.uuid4().hex
        label = "network11"
        tenant_id = uuid.uuid4().hex
        m_t.return_value = tenant_id
        resp = fakes_network.create_fake_json_resp(
            {"network": {"id": id, "label": label,
                         "cidr": address,
                         "gateway": gateway}}, 200
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m_rq.return_value = req_mock
        ret = self.helper.get_network_details(None, id)
        self.assertEqual(id, ret["id"])
        self.assertEqual(address, ret["address"])
        self.assertEqual(gateway, ret["gateway"])
        self.assertEqual(label, ret["name"])
        m_rq.assert_called_with(
            None, method="GET",
            path="/%s/os-networks/%s" % (tenant_id, id),
        )

    @mock.patch.object(helpers.OpenStackHelper, "_get_req")
    @mock.patch.object(helpers.OpenStackHelper, "tenant_from_req")
    def test_create_net(self, m_t, m_rq):
        tenant_id = uuid.uuid4().hex
        m_t.return_value = tenant_id
        name = "name_net"
        net_id = uuid.uuid4().hex
        cidr = "0.0.0.0"
        gateway = "0.0.0.1"
        parameters = {"label": name,
                      "cidr": cidr,
                      "gateway": gateway
                      }
        resp = fakes_network.create_fake_json_resp(
            {"network": {"id": net_id, "label": name,
                         "cidr": cidr,
                         "gateway": gateway}}, 200
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m_rq.return_value = req_mock
        ret = self.helper.create_network(None,
                                         name=name,
                                         cidr=cidr,
                                         gateway=gateway,
                                         )
        body = utils.make_body('network', parameters)
        m_rq.assert_called_with(
            None, method="POST",
            content_type='application/json',
            path="/%s/os-networks" % (tenant_id),
            body=json.dumps(body)
        )
        self.assertEqual(cidr, ret['address'])
        self.assertEqual(name, ret['name'])
        self.assertEqual(gateway, ret['gateway'])
        self.assertEqual(net_id, ret['id'])

    @mock.patch.object(helpers.OpenStackHelper, "_get_req")
    @mock.patch.object(helpers.OpenStackHelper, "tenant_from_req")
    def test_delete_net(self, m_t, m_rq):
        tenant_id = uuid.uuid4().hex
        m_t.return_value = tenant_id
        net_id = uuid.uuid4().hex
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = []
        m_rq.return_value = req_mock
        ret = self.helper.delete_network(None, net_id)
        self.assertEqual(ret, [])
        m_rq.assert_called_with(
            None, method="DELETE",
            path="/%s/os-networks/%s" % (tenant_id, net_id),
        )

    @mock.patch.object(helpers.OpenStackHelper, "index")
    @mock.patch.object(helpers.OpenStackHelper, "get_server")
    @mock.patch.object(helpers.OpenStackHelper, "_get_ports")
    @mock.patch.object(helpers.OpenStackHelper, "get_floating_ips")
    def test_list_compute_net_links(self, m_float, m_ports, m_servers,
                                    m_list_server):
        tenant = fakes.tenants["baz"]
        servers = fakes.servers[tenant["id"]]
        floating_ips = fakes.floating_ips[tenant["id"]]
        ports = fakes.ports[tenant["id"]]
        m_servers.side_effect = servers
        m_list_server.return_value = servers
        m_ports.return_value = ports
        m_float.return_value = floating_ips

        resp = self.helper.list_compute_net_links(None)

        expected = []
        for server in servers:
            server_addrs = server.get("addresses", {})
            instance_vm = server["id"]
            for addr_set in server_addrs.values():
                for addr in addr_set:
                    mac = addr["OS-EXT-IPS-MAC:mac_addr"]
                    ip_type = addr["OS-EXT-IPS:type"]
                    address = addr['addr']
                    net_id = None
                    pool = None
                    public_ip = False
                    if ip_type == "fixed":
                        for p in ports:
                            if p["mac_addr"] == mac:
                                net_id = p['net_id']
                                ip_id = p['port_id']
                                break
                    else:
                        for floating_ip in floating_ips:
                            if floating_ip["ip"] == address:
                                net_id = floating_ip['id']
                                ip_id = floating_ip['id']
                                public_ip = True
                                pool = floating_ip["pool"]
                                break
                    expected.append(
                        {"network_id": net_id,
                         "ip": address,
                         "state": "active",
                         "compute_id": instance_vm,
                         "public_ip": public_ip,
                         "mac": mac,
                         "ip_id":ip_id,
                         "pool": pool}
                    )

        self.assertEquals(expected, resp)

    @mock.patch.object(helpers.OpenStackHelper, "get_server")
    @mock.patch.object(helpers.OpenStackHelper, "_get_ports")
    @mock.patch.object(helpers.OpenStackHelper, "get_floating_ips")
    def test_get_compute_net_link_private(self, m_float, m_ports, m_server):
        tenant = fakes.tenants["baz"]
        server = fakes.servers[tenant["id"]][0]
        floating_ips = fakes.floating_ips[tenant["id"]]
        ports = fakes.ports[tenant["id"]]
        m_server.return_value = server
        m_ports.return_value = ports
        m_float.return_value = floating_ips
        expected = []
        server_addrs = server.get("addresses", {})
        instance_vm = server["id"]
        net_id = uuid.uuid4().hex
        address = "192.168.253.1"
        resp = self.helper.get_compute_net_link(None,
                                                instance_vm,
                                                network_id=net_id,
                                                address=address,
                                                )
        for addr_set in server_addrs.values():
            for addr in addr_set:
                if addr["addr"] == address:
                    mac = addr["OS-EXT-IPS-MAC:mac_addr"]
                    ip_type = addr["OS-EXT-IPS:type"]
                    net_id = None
                    pool = None
                    public_ip = False
                    if ip_type == "fixed":
                        for p in ports:
                            if p["mac_addr"] == mac:
                                net_id = p['net_id']
                                ip_id = p['port_id']
                                break
                    else:
                        for floating_ip in floating_ips:
                            if floating_ip["ip"] == address:
                                net_id = floating_ip['id']
                                ip_id = floating_ip['id']
                                public_ip = True
                                pool = floating_ip["pool"]
                                break
                    expected.append(
                        {"network_id": net_id,
                         "ip": address,
                         "state": "active",
                         "compute_id": instance_vm,
                         "public_ip": public_ip,
                         "mac": mac,
                         "ip_id":ip_id,
                         "pool": pool}
                    )
        self.assertEquals(expected, [resp])

    @mock.patch.object(helpers.OpenStackHelper, "get_server")
    @mock.patch.object(helpers.OpenStackHelper, "_get_ports")
    @mock.patch.object(helpers.OpenStackHelper, "get_floating_ips")
    def test_get_compute_net_link_ipres(self, m_float, m_ports, m_server):
        tenant = fakes.tenants["baz"]
        server = fakes.servers[tenant["id"]][0]
        floating_ips = fakes.floating_ips[tenant["id"]]
        ports = fakes.ports[tenant["id"]]
        m_server.return_value = server
        m_ports.return_value = ports
        m_float.return_value = floating_ips
        expected = []
        server_addrs = server.get("addresses", {})
        instance_vm = server["id"]
        net_id = uuid.uuid4().hex
        address = "200.20.20.2"
        resp = self.helper.get_compute_net_link(None,
                                                instance_vm,
                                                network_id=net_id,
                                                address=address,
                                                )
        for addr_set in server_addrs.values():
            for addr in addr_set:
                if addr["addr"] == address:
                    mac = addr["OS-EXT-IPS-MAC:mac_addr"]
                    ip_type = addr["OS-EXT-IPS:type"]
                    net_id = None
                    pool = None
                    public_ip = False
                    if ip_type == "fixed":
                        for p in ports:
                            if p["mac_addr"] == mac:
                                net_id = p['net_id']
                                ip_id = p['port_id']
                                break
                    else:
                        for floating_ip in floating_ips:
                            if floating_ip["ip"] == address:
                                net_id = floating_ip['id']
                                ip_id = floating_ip['id']
                                public_ip = True
                                pool = floating_ip["pool"]
                                break
                    expected.append(
                        {"network_id": net_id,
                         "ip": address,
                         "state": "active",
                         "compute_id": instance_vm,
                         "public_ip": public_ip,
                         "mac": mac,
                         "ip_id":ip_id,
                         "pool": pool}
                    )

        self.assertEquals(expected, [resp])