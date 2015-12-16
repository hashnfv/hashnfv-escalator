==========
Background
==========

Upgrade Objects
===============

Physical Resource
^^^^^^^^^^^^^^^^^

Most cloud infrastructures support the dynamic addition and removal of
hardware. Accordingly a hardware upgrade could be done by adding the new
piece of hardware and removing the old one. From the persepctive of smooth
upgrade the orchestration/scheduling of these actions is the primary concern.

Upgrading a physical resource may involve as well the upgrade of its firmware
and/or modifying its configuration data. This may require the restart of the
hardware.

Virtual Resources
^^^^^^^^^^^^^^^^^

Addition and removal of virtual resources may be initiated by the users or be
a result of an elasticity action. Users may also request the upgrade of their
virtual resources using a new VM image.

.. Needs to be moved to requirement section: Escalator should facilitate such an
   option and allow for a smooth upgrade.

On the other hand changes in the infrastructure, namely, in the hardware and/or
the virtualization facility resources may result in the upgrade of the virtual
resources. For example if by some reason the hypervisor is changed and
the current VMs cannot be migrated to the new hypervisor - they are
incompatible - then the VMs need to be upgraded too. This is not
something the NFVI user (i.e. VNFs ) would know about.


Virtualization Facility Resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Based on the functionality they provide, virtualization facility
resources could be divided into computing node, networking node,
storage node and management node.

The possible upgrade objects in these nodes are considered below:
(Note: hardware based virtualization may be considered as virtualization
facility resource, but from escalator perspective, it is better to
consider it as part of the hardware upgrade. )

**Computing node**

1. OS Kernel

2. Hypvervisor and virtual switch

3. Other kernel modules, like drivers

4. User space software packages, like nova-compute agents and other
   control plane programs.

Updating 1 and 2 will cause the loss of virtualzation functionality of
the compute node, which may lead to the interruption of data plane services
if the virtual resource is not redudant.

Updating 3 might have the same result.

Updating 4 might lead to control plane services interruption if not an
HA deployment.

.. <MT> I'm not sure why would 4 cause control plane interruption on a
   compute node. My understanding is that simply the node cannot be managed.
   Redundancy won't help in that either.


**Networking node**

1. OS kernel, optional, not all switches/routers allow the upgrade their
   OS since it is more like a firmware than a generic OS.

2. User space software package, like neutron agents and other control
   plane programs

Updating 1 if allowed will cause a node reboot and therefore leads to
data plane service interruption if the virtual resource is not
redundant.

Updating 2 might lead to control plane services interruption if not an
HA deployment.

**Storage node**

1. OS kernel, optional, not all storage nodes allow the upgrade their OS
   since it is more like a firmware than a generic OS.

2. Kernel modules

3. User space software packages, control plane programs

Updating 1 if allowed will cause a node reboot and therefore leads to
data plane services interruption if the virtual resource is not
redundant.

Update 2 might result in the same.

Updating 3 might lead to control plane services interruption if not an
HA deployment.

**Management node**

1. OS Kernel

2. Kernel modules, like driver

3. User space software packages, like database, message queue and
   control plane programs.

Updating 1 will cause a node reboot and therefore leads to control
plane services interruption if not an HA deployment. Updating 2 might
result in the same.

Updating 3 might lead to control plane services interruption if not an
HA deployment.

Upgrade Granularity
===================

The granularity of an upgrade can be characterized from two perspective:
- the physical dimension and
- the software dimension

Physical Dimension
^^^^^^^^^^^^^^^^^^

The physical dimension characterizes the number of similar upgrade objects
targeted by the upgrade, i.e. whether it is full / partial upgrade of a
data centre, cluster, zone.
Because of the upgrade of a data centre or a zone, it may be divided into
several batches. Thus there is a need for efficiency in the execution of
upgrades of potentially huge number of upgrade objects while still maintain
availability to fulfill the requirement of smooth upgrade.

The upgrade of a cloud environment (cluster) may also
be partial. For example, in one cloud environment running a number of
VNFs, we may just try to upgrade one of them to check the stability and
performance, before we upgrade all of them.
Thus there is a need for proper organization of the artifacts associated with
the different upgrade objects. Also the different versions should be able
to coextist beyond the upgrade period.

From this perspective special attention may be needed when upgrading
objects that are collaborating in a redundancy schema as in this case
different versions not only need to coexist but also collaborate. This
puts requirement on the upgrade objects primarily. If this is not possible
the upgrade campaign should be designed in such a way that the proper
isolation is ensured.

Software Dimension
^^^^^^^^^^^^^^^^^^

The software dimension of the upgrade characterizes the upgrade object
type targeted and the combination in which they are upgraded together.

Even though the upgrade may
initially target only one type of upgrade object, e.g. the hypervisor
the dependency of other upgrade objects on this initial target object may
require their upgrade as well. I.e. the upgrades need to be combined. From this
perspective the main concern is compatibility of the dependent and
sponsor objects. To take into consideration of these dependencies
they need to be described together with the version compatility information.
Breaking dependencies is the major cause of outages during upgrades.

In other cases it is more efficient to upgrade a combination of upgrade
objects than to do it one by one. One aspect of the combination is how
the upgrade packages can be combined, whether a new image can be created for
them before hand or the different packages can be installed during the upgrade
independently, but activated together.

The combination of upgrade objects may span across
layers (e.g. software stack in the host and the VM of the VNF).
Thus, it may require additional coordination between the management layers.

With respect to each upgrade object type and even stacks we can
distingush major and minor upgrades:

**Major Upgrade**

Upgrades between major releases may introducing significant changes in
function, configuration and data, such as the upgrade of OPNFV from
Arno to Brahmaputra.

**Minor Upgrade**

Upgrades inside one major releases which would not leads to changing
the structure of the platform and may not infect the schema of the
system data.

Scope of Impact
===============

Considering availability and therefore smooth upgrade, one of the major
concerns is the predictability and control of the outcome of the different
upgrade operations. Ideally an upgrade can be performed without impacting any
entity in the system, which means none of the operations change or potentially
change the behaviour of any entity in the system in an uncotrolled manner.
Accordingly the operations of such an upgrade can be performed any time while
the system is running, while all the entities are online. No entity needs to be
taken offline to avoid such adverse effects. Hence such upgrade operations
are referred as online operations. The effects of the upgrade might be activated
next time it is used, or may require a special activation action such as a
restart. Note that the activation action provides more control and predictability.

If an entity's behavior in the system may change due to the upgrade it may
be better to take it offline for the time of the relevant upgrade operations.
The main question is however considering the hosting relation of an upgrade
object what hosted entities are impacted. Accordingly we can identify a scope
which is impacted by taking the given upgrade object offline. The entities
that are in the scope of impact may need to be taken offline or moved out of
this scope i.e. migrated.

If the impacted entity is in a different layer managed by another manager
this may require coordination because taking out of service some
infrastructure resources for the time of their upgrade which support virtual
resources used by VNFs that should not experience outages. The hosted VNFs
may or may not allow for the hot migration of their VMs. In case of migration
the VMs placement policy should be considered.

