# -*- coding: utf-8 -*-

# Copyright 2015 Spanish National Research Council
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

from ooi.api import base
import ooi.wsgi


class Controller(base.Controller):
    def index(self, req):
        tenant_id = req.environ["keystone.token_auth"].user.project_id
        req.path_info = "/%s/servers" % tenant_id
        return req.get_response(self.app)


def create_resource(app):
    return ooi.wsgi.Resource(Controller(app))
