General Requirements Background and Terminology
-----------------------------------------------

Terminologies and definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NFVI
  The term is an abbreviation for Network Function Virtualization
  Infrastructure; sometimes it is also referred as data plane in this
  document. The NFVI provides the virtual resources to the virtual
  network functions under the control of the VIM.

VIM
  The term is an abbreviation for Virtual Infrastructure Manager;
  sometimes it is also referred as control plane in this document.
  The VIM controls and manages the NFVI compute, network and storage
  resources to provide the required virtual resources to the VNFs.

Operator
  The term refers to network service providers and Virtual Network
  Function (VNF) providers.

End-User
  The term refers to a subscriber of the Operator's services.

Network Service
  The term refers to a service provided by an Operator to its
  end-users using a set of (virtualized) Network Functions

Infrastructure Services
  The term refers to services provided by the NFV Infrastructure to the VNFs
  as required by the Management & Orchestration functions and especially the VIM.
  I.e. these are the virtual resources as perceived by the VNFs.

Smooth Upgrade
  The term refers to an upgrade that results in no service outage
  for the end-users.

Rolling Upgrade
  The term refers to an upgrade strategy, which upgrades a node or a subset
  of nodes at a time in a wave style rolling through the data centre. It
  is a popular upgrade strategy to maintain service availability.

Parallel Universe Upgrade
  The term refers to an upgrade strategy, which creates and deploys
  a new universe - a system with the new configuration - while the old
  system continues running. The state of the old system is transferred
  to the new system after sufficient testing of the new system.

Infrastructure Resource Model
  The term refers to the representation of infrastructure resources,
  namely: the physical resources, the virtualization
  facility resources and the virtual resources.

Physical Resource
  The term refers to a piece of hardware in the NFV infrastructure that may
  also include firmware enabling this piece of hardware.

Virtual Resource
  The term refers to a resource, which is provided as services built on top
  of the physical resources via the virtualization facilities; in particular,
  virtual resources are the resources on which VNFs are deployed. Examples of
  virtual resources are: VMs, virtual switches, virtual routers, virtual disks.

Visualization Facility
  The term refers to a resource that enables the creation
  of virtual environments on top of the physical resources, e.g.
  hypervisor, OpenStack, etc.

Upgrade Campaign
  The term refers to a choreography that describes how the upgrade should
  be performed in terms of its targets (i.e. upgrade objects), the
  steps/actions required of upgrading each, and the coordination of these
  steps so that service availability can be maintained. It is an input to an
  upgrade tool (Escalator) to carry out the upgrade.

Upgrade Duration
  The duration of an upgrade characterized by the time elapsed between its
  initiation and its completion. E.g. from the moment the execution of an
  upgrade campaign has started until it has been committed. Depending on
  the upgrade strategy, the state of the configuration and the upgrade target
  some parts of the system may be in a more vulnerable state with respect to
  service availbility.

Outage
  The period of time during which a given service is not provided is referred
  as the outage of that given service. If a subsystem or the entire system
  does not provide any service, it is the outage of the given subsystem or the
  system. Smooth upgrade means upgrade with no outage for the user plane, i.e.
  no VNF should experience service outage.

Rollback
  The term refers to a failure handling strategy that reverts the changes
  done by a potentially failed upgrade execution one by one in a reverse order.
  I.e. it is like undoing the changes done by the upgrade.

Backup
  The term refers to data persisted to a storage, so that it can be used to
  restore the system or a given part of it in the same state as it was when the
  backup was created assuming a cold restart. Changes made to the system from
  the moment the backup was created till the moment it is used to restore the
  (sub)system are lost in the restoration process.

Restore
  The term refers to a failure handling strategy that reverts the changes
  done, for example, by an upgrade by restoring the system from some backup
  data. This results in the loss of any change and data persisted after the
  backup was been taken. To recover those additional measures need to be taken
  if necessary (e.g. rollforward).

Rollforward
  The term refers to a failure handling strategy applied after a restore
  (from a backup) opertaion to recover any loss of data persisted between
  the time the backup has been taken and the moment it is restored. Rollforward
  requires that data that needs to survive the restore operation is logged at
  a location not impacted by the restore so that it can be re-applied to the
  system after its restoration from the backup.

Downgrade
  The term refers to an upgrade in which an earlier version of the software
  is restored through the upgrade procedure. A system can be downgraded to any
  earlier version and the compatibility of the versions will determine the
  applicable upgrade strategies and whether service outage can be avoided.
  In particular any data conversion needs special attention.



Upgrade Objects
~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~

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



Upgrade duration
~~~~~~~~~~~~~~~~

As the OPNFV end-users are primarily Telecom operators, the network
services provided by the VNFs deployed on the NFVI should meet the
requirement of 'Carrier Grade'.::

  In telecommunication, a "carrier grade" or"carrier class" refers to a
  system, or a hardware or software component that is extremely reliable,
  well tested and proven in its capabilities. Carrier grade systems are
  tested and engineered to meet or exceed "five nines" high availability
  standards, and provide very fast fault recovery through redundancy
  (normally less than 50 milliseconds). [from wikipedia.org]

"five nines" means working all the time in ONE YEAR except 5'15".

::

  We have learnt that a well prepared upgrade of OpenStack needs 10
  minutes. The major time slot in the outage time is used spent on
  synchronizing the database. [from ' Ten minutes OpenStack Upgrade? Done!
  ' by Symantec]

This 10 minutes of downtime of the OpenStack services however did not impact the
users, i.e. the VMs running on the compute nodes. This was the outage of
the control plane only. On the other hand with respect to the
preparations this was a manually tailored upgrade specific to the
particular deployment and the versions of each OpenStack service.

The project targets to achieve a more generic methodology, which however
requires that the upgrade objects fulfil certain requirements. Since
this is only possible on the long run we target first the upgrade
of the different VIM services from version to version.

**Questions:**

1. Can we manage to upgrade OPNFV in only 5 minutes?
 
.. <MT> The first question is whether we have the same carrier grade
   requirement on the control plane as on the user plane. I.e. how
   much control plane outage we can/willing to tolerate?
   In the above case probably if the database is only half of the size
   we can do the upgrade in 5 minutes, but is that good? It also means
   that if the database is twice as much then the outage is 20
   minutes.
   For the user plane we should go for less as with two release yearly
   that means 10 minutes outage per year.

.. <Malla> 10 minutes outage per year to the users? Plus, if we take
   control plane into the consideration, then total outage will be
   more than 10 minute in whole network, right?

.. <MT> The control plane outage does not have to cause outage to
   the users, but it may of course depending on the size of the system
   as it's more likely that there's a failure that needs to be handled
   by the control plane.

2. Is it acceptable for end users ? Such as a planed service
   interruption will lasting more than ten minutes for software
   upgrade.

.. <MT> For user plane, no it's not acceptable in case of
   carrier-grade. The 5' 15" downtime should include unplanned and
   planned downtimes.
   
.. <Malla> I go agree with Maria, it is not acceptable.

3. Will any VNFs still working well when VIM is down?

.. <MT> In case of OpenStack it seems yes. .:)

The maximum duration of an upgrade
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The duration of an upgrade is related to and proportional with the
scale and the complexity of the OPNFV platform as well as the
granularity (in function and in space) of the upgrade.

.. <Malla> Also, if is a partial upgrade like module upgrade, it depends
  also on the OPNFV modules and their tight connection entities as well.

.. <MT> Since the maintenance window is shrinking and becoming non-existent
  the duration of the upgrade is secondary to the requirement of smooth upgrade.
  But probably we want to be able to put a time constraint on each upgrade
  during which it must complete otherwise it is considered failed and the system
  should be rolled back. I.e. in case of automatic execution it might not be clear
  if an upgrade is long or just hanging. The time constraints may be a function
  of the size of the system in terms of the upgrade object(s).

The maximum duration of a roll back when an upgrade is failed 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The duration of a roll back is short than the corresponding upgrade. It
depends on the duration of restore the software and configure data from
pre-upgrade backup / snapshot.

.. <MT> During the upgrade process two types of failure may happen:
  In case we can recover from the failure by undoing the upgrade
  actions it is possible to roll back the already executed part of the
  upgrade in graceful manner introducing no more service outage than
  what was introduced during the upgrade. Such a graceful roll back
  requires typically the same amount of time as the executed portion of
  the upgrade and impose minimal state/data loss.
  
.. <MT> Requirement: It should be possible to roll back gracefully the
  failed upgrade of stateful services of the control plane.
  In case we cannot recover from the failure by just undoing the
  upgrade actions, we have to restore the upgraded entities from their
  backed up state. In other terms the system falls back to an earlier
  state, which is typically a faster recovery procedure than graceful
  roll back and depending on the statefulness of the entities involved it
  may result in significant state/data loss.
  
.. <MT> Two possible types of failures can happen during an upgrade

.. <MT> We can recover from the failure that occurred in the upgrade process:
  In this case, a graceful rolling back of the executed part of the
  upgrade may be possible which would "undo" the executed part in a
  similar fashion. Thus, such a roll back introduces no more service
  outage during an upgrade than the executed part introduced. This
  process typically requires the same amount of time as the executed
  portion of the upgrade and impose minimal state/data loss.

.. <MT> We cannot recover from the failure that occurred in the upgrade
   process: In this case, the system needs to fall back to an earlier
   consistent state by reloading this backed-up state. This is typically
   a faster recovery procedure than the graceful roll back, but can cause
   state/data loss. The state/data loss usually depends on the
   statefulness of the entities whose state is restored from the backup.

The maximum duration of a VNF interruption (Service outage)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since not the entire process of a smooth upgrade will affect the VNFs,
the duration of the VNF interruption may be shorter than the duration
of the upgrade. In some cases, the VNF running without the control
from of the VIM is acceptable.

.. <MT> Should require explicitly that the NFVI should be able to
  provide its services to the VNFs independent of the control plane?

.. <MT> Requirement: The upgrade of the control plane must not cause
  interruption of the NFVI services provided to the VNFs.

.. <MT> With respect to carrier-grade the yearly service outage of the
  VNF should not exceed 5' 15" regardless whether it is planned or
  unplanned outage. Considering the HA requirements TL-9000 requires an
  end-to-end service recovery time of 15 seconds based on which the ETSI
  GS NFV-REL 001 V1.1.1 (2015-01) document defines three service
  availability levels (SAL). The proposed example service recovery times
  for these levels are:

.. <MT> SAL1: 5-6 seconds

.. <MT> SAL2: 10-15 seconds

.. <MT> SAL3: 20-25 seconds

.. <Pva> my comment was actually that the downtime metrics of the
  underlying elements, components and services are small fraction of the
  total E2E service availability time. No-one on the E2E service path
  will get the whole downtime allocation (in this context it includes
  upgrade process related outages for the services provided by VIM etc.
  elements that are subject to upgrade process).
  
.. <MT> So what you are saying is that the upgrade of any entity
  (component, service) shouldn't cause even this much service
  interruption. This was the reason I brought these figures here as well
  that they are posing some kind of upper-upper boundary. Ideally the
  interruption is in the millisecond range i.e. no more than a
  switch-over or a live migration.
  
.. <MT> Requirement: Any interruption caused to the VNF by the upgrade
  of the NFVI should be in the sub-second range.

.. <MT]> In the future we also need to consider the upgrade of the NFVI,
  i.e. HW, firmware, hypervisors, host OS etc.