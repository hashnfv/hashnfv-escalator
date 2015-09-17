Use Cases and Scenarios
-----------------------

This section describes the use cases and scenarios to verify the 
requirements of Escalator.

Upgrade a system with minimal configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A minimal configuration system is normally deployed for experimental or
development usages, such as a OPNFV test bed.  Although it dose not have
large workload, but it is a typical system to be upgraded frequently.

Upgrade a system with HA configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A HA configuration system is very popular in the operator's data centre.
And it is a typical product environment. It always running 7 \* 24 a
week with VNFs running on it to provide services to the end users.

Upgrade a system with Multi-Site configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upgrade in one site may cause service interruption to other site, if
both sites are depended and sharing the same modules/data base (e.g. a
keystone for both sites).

If a site failure during an upgrade, the roll-back missing any minimal
state/data loss can cause an affect/failure to the depended site.

==Consider one site of ARNO release first. Then, multi-site in the
future.==