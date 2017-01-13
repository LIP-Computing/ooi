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


try:
    from oslo_config import cfg
except ImportError:
    from oslo.config import cfg  # noqa


def parse_args(argv, default_config_files=None):
    cfg.CONF(argv[1:],
             project='ooi',
             default_config_files=default_config_files)
