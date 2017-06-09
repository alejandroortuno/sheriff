import boto3
import ipaddress
from optparse import OptionParser


AWS_INGRESS_EGRESS_KEYS = {'IpPermissionsEgress': 'Egress',
                           'IpPermissions': 'Ingress'}


def is_ip_on_cidr(ip_to_check, cidr_network):
    """
        Returns True if the ip belongs the network and false otherwise
    """
    ip_address = ipaddress.ip_network(ip_to_check)
    ip_network = ipaddress.ip_network(cidr_network)
    return ip_network.overlaps(ip_address)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ip", dest="ip_to_check",
                      help="IP to check")
    (options, args) = parser.parse_args()

    ip_to_check = options.ip_to_check

    #Use different sessions for the AWS config file Keys
    session = boto3.Session(profile_name='test')
    ec2 = session.client('ec2')
    security_groups = ec2.describe_security_groups()

    for key in AWS_INGRESS_EGRESS_KEYS.keys():
        # Ingress
        for sg in security_groups['SecurityGroups']:
            for ip_rules in sg[key]:
                for range in ip_rules['IpRanges']:
                    if 'CidrIp' in range.keys():
                        if is_ip_on_cidr(unicode(ip_to_check), unicode(range['CidrIp'])):
                            from_port = 'any'if 'FromPort' not in ip_rules.keys() else str(ip_rules['FromPort'])
                            to_port = 'any' if 'ToPort' not in ip_rules.keys() else str(ip_rules['ToPort'])
                            print sg['GroupId'] + ':' + AWS_INGRESS_EGRESS_KEYS[key] + ':' + from_port + ':' + to_port
