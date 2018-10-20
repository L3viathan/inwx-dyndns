#!/usr/bin/env python
# -*- encoding: UTF8 -*-

# authors: L3viathan, github.com/L3viathan
#          Philipp Klaus, philipp.klaus →AT→ gmail.com

# This file is part of inwx-dyndns
#
# inwx-dyndns is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# inwx-dyndns is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with inwx-dyndns. If not, see <http://www.gnu.org/licenses/>.

# This is obviously heavily borrowed (almost everything is the same) from Philipp Klaus' python-inwx-xmlrpc.

import os
import time
from inwx import domrobot
from configuration import get_account_data, get_domain_update

MINUTES = 15

while True:
    api_url, username, password = get_account_data(True)
    domain, subdomain, default_ip = get_domain_update(True)
    with open(os.environ.get("IPv4_PATH")) as f:
        new_ip = f.read()

    inwx_conn = domrobot(api_url, username, password, "en", False)
    nsentries = inwx_conn.nameserver.info({"domain": domain})
    ids = []
    for record in nsentries["record"]:
        if record["name"] in ["", "*"]:
            ids.append(record["id"])
    for id_ in ids:
        print("Setting subdomain %s to the new IPv4 IP %s." % (subdomain, new_ip))
        inwx_conn.nameserver.updateRecord({"id": id_, "content": new_ip, "ttl": 3600})
    print(f"Going to sleep for {MINUTES} minutes")
    time.sleep(MINUTES * 60)
