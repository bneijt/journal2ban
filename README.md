Introduction
------------
Simple python script that will follow the systemd journal via the
systemd-journal-gatewayd to listen for authentication failures on
the sshd.service.

Upon any authenticaiton failure, ipset is called to add the IPv4 or IPv6 address to `blackfour` and `blacksix` respectively.

The current logic is as follows:

 - Follow journal messages from `_SYSTEMD_UNIT=sshd.service`
 - If the message contains "authentication failure", regex match the rhost out of the line
   - If `rhost` is an IPv4 address, call `ipset -exist add blackfour`
   - Else if `rhost` is an IPv6 address, call `ipset -exist add blacksix`
   - Else log an error about parsing the line

Installation
------------
To use journal2ban.py you have to first the ipsets `blackfour` and `blacksix`, for example using the `ipset.conf` distributed with this package.

This requires the installation of the ipsets tools.

Secondly, you need to add a firewall rule to block the users, for example, of the IPv4 table:

    -A INPUT -m set --match-set blackfour src -j DROP

And for the IPv6 table:

    -A INPUT -m set --match-set blacksix src -j DROP

Examples can also be found in the `ip6tables.rules` file and `iptables.rules` file.


