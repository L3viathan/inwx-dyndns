#!/usr/bin/env python
# -*- encoding: UTF8 -*-

# author: Philipp Klaus, philipp.klaus →AT→ gmail.com
# author: InterNetworX, info →AT→ inwx.de

# This file is part of python-inwx-xmlrpc.
#
# python-inwx-xmlrpc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-inwx-xmlrpc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-inwx-xmlrpc. If not, see <http://www.gnu.org/licenses/>.


#####################################################################
######   This the most important file of the project:         #######
######   It contains the classes inwx and domrobot, which     #######
######   implement the XML-RPC communication with the         #######
######   InterNetworX API.                                    #######

from xmlrpc.client import ServerProxy, Fault, ProtocolError, _Method, SafeTransport


class domrobot(ServerProxy):
    def __init__(
        self, address, username=None, password=None, language="en", verbose=False
    ):
        self.__address = address
        ServerProxy.__init__(
            self, address, transport=InwxTransport(), encoding="UTF-8", verbose=verbose
        )
        self.account.login({"lang": language, "user": username, "pass": password})

    def __getattr__(self, name):
        return _Method(self.__request, name)

    def __request(self, methodname, params):
        method_function = ServerProxy.__getattr__(self, methodname)
        self.__params = dict()
        if (
            params
            and isinstance(params, tuple)
            and isinstance(params[0], dict)
        ):
            self.__params.update(params[0])

        try:
            response = method_function(self.__params)
        except Fault as err:
            raise NameError("Fault", err)
        except ProtocolError as err:
            raise NameError("ProtocolError", err)
        except Exception as err:
            raise NameError(
                "Some other error occured, presumably with the network connection to %s"
                % self.__address,
                err,
            )
        if response["code"] < 2000:
            try:
                return response["resData"]
            except:
                # not all requests send a response
                return None
        else:
            raise NameError(
                "There was a problem: %s (Error code %s)"
                % (response["msg"], response["code"]),
                response,
            )


##
# Adds Cookie support to the SafeTransport class:


class InwxTransport(SafeTransport):
    user_agent = "DomRobot/1.0 Python python-inwx-xmlrpc"
    __cookie = None

    def single_request(self, host, handler, request_body, verbose=0):
        # This method is almost the same as:
        # http://hg.python.org/cpython/file/2.7/Lib/xmlrpclib.py#l1281

        h = self.make_connection(host)
        if verbose:
            h.set_debuglevel(1)

        try:
            self.send_request(h, handler, request_body)
            self.send_host(h, host)
            self.send_user_agent(h)
            self.send_content(h, request_body)

            response = h.getresponse(buffering=True)
            if response.status == 200:
                self.verbose = verbose
                cookie_header = response.getheader("set-cookie")
                if cookie_header:
                    self.__cookie = cookie_header
                return self.parse_response(response)
        except Fault:
            raise
        except Exception:
            # All unexpected errors leave connection in
            # a strange state, so we clear it.
            self.close()
            raise
        # discard any response data and raise exception
        if response.getheader("content-length", 0):
            response.read()
        raise ProtocolError(
            host + handler, response.status, response.reason, response.msg
        )

    def send_content(self, connection, request_body):
        # This method is almost the same as:
        # http://hg.python.org/cpython/file/2.7/Lib/xmlrpclib.py#l1428
        connection.putheader("Content-Type", "text/xml")
        connection.putheader("Content-Length", str(len(request_body)))
        if self.__cookie:
            connection.putheader("Cookie", self.__cookie)
        connection.endheaders(request_body)
