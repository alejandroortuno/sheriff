# sheriff
Find AWS security groups that contains an specific network range.

Ensure you configure profiles for the AWS access keys: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

Example to run the tool: ./sheriff.py -i '192.168.0.0/24'

Tool output is in the form:

Security Group ID:Direction of traffic:From port:To port

Example
sg-xxxxx:Ingress:22:22
sg-yyyyy:Ingress:5500:5500
sg-zzz:Egress:443:443
