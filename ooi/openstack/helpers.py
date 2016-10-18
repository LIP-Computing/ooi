# -*- coding: utf-8 -*-

# Copyright 2015 Spanish National Research Council
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

from ooi.occi import helpers

_PREFIX = "http://schemas.openstack.org/"
PUBLIC_NETWORK = "PUBLIC"


def build_scheme(category):
    return helpers.build_scheme(category, prefix=_PREFIX)


def vm_state(nova_status):
    if nova_status == "ACTIVE":
        return "active"
    elif nova_status == "SUSPENDED":
        return "suspended"
    else:
        return "inactive"


# TODO(enolfc): Do really implement this.
def vol_state(nova_status):
    return "online"


def network_status(neutron_status):
    """Translate neutron network status.

    :param neutron_status: neutron status
    """
    if neutron_status == "ACTIVE":
        return "active"
    else:
        return "inactive"


def security_group_rule_type(neutron_type):
    """Translate neutron rule type.

    :param neutron_type: neutron status
    """
    if neutron_type == "ingress":
        return "inbound"
    else:
        return "outbound"


def build_security_group_from_neutron(sec_groups):
    """Translate neutron security groups to ooi standard
    security group format.

    :param sec_groups: array of security groups
    """
    sec_list = []
    for sec in sec_groups:
        ooi_sec = {}
        rules_list = []
        ooi_sec["id"] = sec["id"]
        ooi_sec["title"] = sec.get("name", None)
        for rule in sec["security_group_rules"]:
            ipversion = rule.get("ethertype", "IPv4")
            rule_type = security_group_rule_type(
                rule["direction"]
            )
            rule_protocol = rule.get("protocol", None)
            rule_port = "%s-%s" % (str(rule["port_range_min"]),
                                   str(rule["port_range_max"])
                                   )
            rule_range = str(rule["remote_ip_prefix"])
            rules_list.append({"type": rule_type,
                               "protocol": rule_protocol,
                               "port": rule_port,
                               "range": rule_range,
                               "ipversion": ipversion}
                              )
        ooi_sec["rules"] = rules_list
        sec_list.append(ooi_sec)
    return sec_list
