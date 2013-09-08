Simple python script that will follow the systemd journal via the
systemd-journal-gatewayd to listen for authentication failures on
the sshd.service.

Upon an authenticaiton failure, ipset is called to add the IPv4 or IPv6 address to `blackfour` and `blacksix` respectively.

