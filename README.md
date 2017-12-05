
This script is registering DNS records for your dynamic gateway IP provided by your ISP.

It checks the current public IP of your gateway and compares against a pre-defined DNS record in a hosted zone in Amazon Route53. 

Make sure you configure the `RECORD` and `DOMAIN` parameters (and of course boto config file).

```
$ python ddns.py
record updated. New IP: xxx.xxx.xxx.xxx
```
