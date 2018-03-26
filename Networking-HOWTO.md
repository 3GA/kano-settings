# Networking in Kanux
## Introduction

KanuxOS system is network ready from first boot, with ipv4 support. This document explains the various options.

Kanux supports the following connectivity devices:

- Ethernet
- WiFi
- Android USB

### Ethernet

Ethernet connectivity should always be ready functioning. Simply plug the network cable to a dhcp-ready network and Kanux will acquire a DHCP lease automatically.

### USB devices

In order to enable the network interface for the USB port to work with tethering you need to do the following: Edit the following file as root `sudo vi /etc/network/interfaces` and add the line `iface usb0 inet dhcp` in the end of the file, which enables the `dhcp` service for the USB port.

After this run `sudo ifup usb0` and reboot. Now enable tethering on your mobile device, just connect it to the Kanux and you should be online!

### WiFi

Raspbian `Jessie` is not following the usual `Debian` approach to networking with`/etc/network/if-*` scripts. Instead `dhcpcd` is used. `dhcpcd` is an implementation of the `DHCP` client specified in `RFC 2131`. It gets the host information (`IP`address, routes, etc) from a `DHCP` server and configures the network interface of the machine on which it is running.

It then runs the configuration script which writes `DNS` information to `resolvconf`, if available, otherwise directly to `/etc/resolv.conf`. If the `hostname` is currently `blank`, (`null`) or `localhost`, or `force_hostname` is `YES` or `TRUE` or `1` then dhcpcd sets the hostname to the one supplied by the `DHCP` server.

`dhcpcd` then daemonises and waits for the lease renewal time to lapse. It will attempt to renew its lease and reconfigure if the new lease changes, when the lease begins to expire, or the `DHCP` server sends message to renew early.

It turns out that `dhcpcd` has a very neat way of hooking up into the network configuration: all you need to do is drop a script in the `/lib/dhcpcd/dhcpcd-hooks` directory, and it will get called at the various stages of the IP allocation process. The script will receive a bunch of useful variables like `${interface}` and `${new_ip_address}` that make it easy to get all the data we need. Check also the `dhcpcd-run-hooks` man page!

#### Graphical

If you need to connect to other wireless networks, open the "Wifi" app icon on the right hand end of the menu bar, or execute "sudo kano-wifi" from the command line. Once you successfully connect to a wireless network, it will be remembered, so next time you boot Kanux it will automatically connect to the network if it is in range.

#### Command Line

In case you need to fine tune more specific wireless secured networks, kano-wifi allows you to provide a custom wpa_supplicant configuration file, like this:

`sudo kano-wifi /path/to/my/wpa_supplicant.conf`

Make sure you provide an absolute path filename to avoid problems during automatic connect at boot time. As an example here's a small simple file to connect to a WPA2 network:

```bash
network={
    ssid="myssid"
    scan_ssid=1
    proto=WPA RSN
  	key_mgmt=WPA-PSK
  	pairwise=CCMP TKIP
  	group=CCMP TKIP
  	psk="mypassword"
}

network={
    ssid="myschoolssid"
    psk="schoolpassword"
    id_str="school"
}
```

The wpa supplicant daemon log file is saved under /var/log/kano_wpa.log where you can find inner details on the association sequence.

If you need to configure the password as a 32 byte hexadecimal number you can use the tool `wpa_passphrase "myssid" "mypassword"`to generate it. As shown in the example, two different networks can be used (for example one for home and one for a school `ssid`.)

### IPv6 support

The kernel has built-in support for IPv6 networking but is disabled by default. To enable it, either `sudo modprobe ipv6` or add `ipv6` in the file `/etc/modules` and restart the system:

- [Raspbian FAQ](http://www.raspbian.org/RaspbianFAQ#How_do_I_enable_or_use_IPv6.3F)

More in-depth information regarding IPv6 and its use in Debian can be found here:

- [Debian IPv6](https://wiki.debian.org/DebianIPv6)
