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

from ooi.occi.core import attribute as attr
from ooi.occi.core import kind
from ooi.occi import helpers
from ooi.occi.infrastructure import network


class IPReservation(network.NetworkResource):
    attributes = attr.AttributeCollection({
        "occi.ipreservation.address": attr.MutableAttribute(
            "occi.ipreservation.address",
            description="Internet Protocol network address",
            attr_type=attr.AttributeType.string_type)})

    kind = kind.Kind(helpers.build_scheme('infrastructure'), 'ipreservation',
                     'IPReservation', attributes, 'ipreservation/',
                     parent=network.NetworkResource.kind)

    def __init__(self, title, address, id=None, state=None, mixins=[]):
        super(IPReservation, self).__init__(title, id=id, state=state,
                                            mixins=mixins)

        self.address = address

    @property
    def address(self):
        return self.attributes["occi.ipreservation.address"].value

    @address.setter
    def address(self, value):
        self.attributes["occi.ipreservation.address"].value = value
