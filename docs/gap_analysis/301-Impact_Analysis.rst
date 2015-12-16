===============
Impact Analysis
===============

Upgrading the different software modules may cause different impact on
the availability of the infrastructure resources and even on the service
continuity of the vNFs.

**Software modules in the computing nodes**

#. Host OS patch

#. Hypervisor, such as KVM, QEMU, XEN, libvirt
#. Openstack agent in computing nodes (like Nova agent, Ceilometer
   agent...)

.. <MT> As SW module, we should list the host OS and maybe its
   drivers as well. From upgrade perspective do we limit host OS
   upgrades to patches only?

**Software modules in network nodes**

#. Neutron L2/L3 agent
#. OVS, SR-IOV Driver

**Software modules storage nodes**

#. Ceph

The table below analyses such an impact - considering a single instance
of each software module - from the following aspects:

-  the function which will be lost during upgrade,
-  the duration of the loss of this specific function,
-  if this causes the loss of the vNF function,
-  if it causes incompatibility in the different parts of the software,
-  what should be backed up before the upgrade,
-  the duration of restoration time if the upgrade fails

These values provided come from internal testing and based on some
assumptions, they may vary depending on the deployment techniques.
Please feel free to add if you find more efficient values during your
testing.

https://wiki.opnfv.org/_media/upgrade_analysis_v0.5.xlsx

Note that no redundancy of the software modules is considered in the table.
