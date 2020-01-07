# vpc

Contains templates for standing up VPC's with CloudFormation

## Designs

* **2 Zone Flat** - VPC with 2 subnets in 2 different zones. No NAT Gateways.
* **3 Zone Public / Private** - (3-zone-pub-priv.yaml) VPC with 3 subnets in 3 zones. 3 NAT Gateways for each private subnet.