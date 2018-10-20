# inwx-dyndns: A Python "tool" based on [python-inwx-xmlrpc](http://github.com/pklaus/python-inwx-xmlrpc) for Dynamic DNS

This is a stripped-down version of pklaus' python-inwx-xmlrpc. Nothing is added, there's just a lot removed and one of his examples renamed and slightly adapted (for use of IPv4).


## Usage

1. Create a copy of the file `python-inwx-xmlrpc.cfg.example` called `python-inwx-xmlrpc.cfg`, and fill in your credentials and the domain. You can leave everything else as-is.
2. Start `python3 inwx-dyndns.py` as a service and give it the location of your IP address as an environment variable as `IPv4_PATH`.

## Licence

I am forced to license this under the GPLv3. For details, see the file `COPYING`.
