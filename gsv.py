#!/usr/bin/env python

from libnmap.parser import NmapParser
import argparse

# Install requirements: pip install python-libnmap

# 
# NAME
#           gsv - Generate nmap version detection command (-sV) from the XML-output file generated by an nmap scan.
#
# SYNOPSIS
#           python3 gsv.py -h
#           python3 gsv.py -x ./nmap_report.xml
#           python3 gsv.py -x ./nmap_report.xml -p ports
# 
# AUTHOR
#           Based on source by pry0cc, https://gist.githubusercontent.com/pry0cc/dd2e7955d0a0222eb6c09cb283a6d614/raw/3c7bd4c20bb7649a944a36507073d9c9ab4100d8/ports.py
#           Further dev. by John Abraham, <pdv.dev07@outlook.com>

def print_ports(ports):
    output = ""
    sorted_ports = sorted(set(ports))
    for p in sorted_ports:
        output += str(p) + ","
    output = output[:-1]
    print(output)

def print_nmap_cmd_sV(host_ip, ports):
    str_ports = ""
    sorted_ports = sorted(set(ports))
    for p in sorted_ports:
        str_ports += str(p) + ","
    cmd = "nmap " + host_ip + " -p " + str_ports[:-1] + " -sV -vv"
    print(cmd)

def main():
    try:
        parser = argparse.ArgumentParser(prog ="gsv", usage="%(prog)s [-h] -x [xml-file] -p [print-option]", description="Generate nmap version detection command (-sV) from the XML-output file generated by an nmap scan.")
        parser._action_groups.pop()
        required = parser.add_argument_group('required arguments')
        required.add_argument('-x', '--xml_file', help='xml file from nmap scan', required=True)
        optional = parser.add_argument_group('optional arguments')
        optional.add_argument('-p', '--print_option', help='print option', default='nmap_cmd', const='nmap_cmd', nargs='?', choices=['nmap_cmd','ports'], required=False)
        optional.add_argument('-v', help="more verbose output", action='store_true', required=False)
        args = parser.parse_args() 

        nmap_report = NmapParser.parse_fromfile(args.xml_file)

        open_and_filtered_ports = []
        opentcp = []
        openudp = []
        openhosts = []
        open_and_filtered_ports = []
        scanned_host_ip = "[null]"

        for h in nmap_report.hosts:
            for s in h.services:
                if s.state != "open|filtered":
                    open_and_filtered_ports.append(s.port)
                    openhosts.append(h.ipv4)
                    if s.protocol == "tcp":
                        opentcp.append(s.port)
                    else:
                        openudp.append(s.port)

                    # TODO: What about multiple IP-scans???
                    # openportprotoserviceversion.append(str(h.ipv4) + ":" + str(s.port))
                    scanned_host_ip = h.ipv4
                    open_and_filtered_ports.append(s.port)            
       
        if args.print_option == 'ports':
            print_ports(open_and_filtered_ports)
        else:
            print_nmap_cmd_sV(scanned_host_ip, open_and_filtered_ports)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()