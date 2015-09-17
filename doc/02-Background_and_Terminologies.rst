General Requirements Background and Terminology
-----------------------------------------------

Terminologies and definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  **NFVI** is abbreviation for Network Function Virtualization
   Infrastructure; sometimes it is also referred as data plane in this
   document.
-  **VIM** is abbreviation for Virtual Infrastructure Management;
   sometimes it is also referred as control plane in this document.
-  **Operators** are network service providers and Virtual Network
   Function (VNF) providers.
-  **End-Users** are subscribers of Operator's services.
-  **Network Service** is a service provided by an Operator to its
   End-users using a set of (virtualized) Network Functions
-  **Infrastructure Services** are those provided by the NFV
   Infrastructure and the Management & Orchestration functions to the
   VNFs. I.e. these are the virtual resources as perceived by the VNFs.
-  **Smooth Upgrade** means that the upgrade results in no service
   outage for the end-users.
-  **Rolling Upgrade** is an upgrade strategy that upgrades each node or
   a subset of nodes in a wave rolling style through the data centre. It
   is a popular upgrade strategy to maintains service availability.
-  **Parallel Universe** is an upgrade strategy that creates and deploys
   a new universe - a system with the new configuration - while the old
   system continues running. The state of the old system is transferred
   to the new system after sufficient testing of the later.
-  **Infrastructure Resource Model** ==(suggested by MT)== is identified
   as: physical resources, virtualization facility resources and virtual
   resources.
-  **Physical Resources** are the hardware of the infrastructure, may
   also includes the firmware that enable the hardware.
-  **Virtual Resources** are resources provided as services built on top
   of the physical resources via the virtualization facilities; in our
   case, they are the components that VNF entities are built on, e.g.
   the VMs, virtual switches, virtual routers, virtual disks etc
   ==[MT] I don't think the VNF is the virtual resource. Virtual
   resources are the VMs, virtual switches, virtual routers, virtual
   disks etc. The VNF uses them, but I don't think they are equal. The
   VIM doesn't manage the VNF, but it does manage virtual resources.==
-  **Visualization Facilities** are resources that enable the creation
   of virtual environments on top of the physical resources, e.g.
   hypervisor, OpenStack, etc.

Upgrade Objects
~~~~~~~~~~~~~~~

Physical Resource
^^^^^^^^^^^^^^^^^

| Most of the cloud infrastructures support dynamic addition/removal of
  hardware. A hardware upgrade could be done by removing the old
  hardware node and adding the new one. Upgrade a physical resource,
  like upgrade the firmware and modify the configuration data, may
  be considered in the future. 

Virtual Resources
^^^^^^^^^^^^^^^^^

| Virtual resource upgrade mainly done by users. OPNFV may facilitate
  the activity, but suggest to have it in long term roadmap instead of
  initiate release.
| ==[MT] same comment here: I don't think the VNF is the virtual
  resource. Virtual resources are the VMs, virtual switches, virtual
  routers, virtual disks etc. The VNF uses them, but I don't think they
  are equal. For example if by some reason the hypervisor is changed and
  the current VMs cannot be migrated to the new hypervisor, they are
  incompatible, then the VMs need to be upgraded too. This is not
  something the NFVI user (i.e. VNFs ) would even know about.==

Virtualization Facility Resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Based on the functionality they provide, virtualization facility
  resources could be divided into computing node, networking node,
  storage node and management node.
| The possible upgrade objects in these nodes are addressed below:
  (Note: hardware based virtualization may considered as virtualization
  facility resource, but from escalator perspective, it is better
  considered it as part of hardware upgrade. )

**Computing node**

1. OS Kernel
2. Hypvervisor and virtual switch
3. Other kernel modules, like driver
4. User space software packages, like nova-compute agents and other
   control plane programs

| Updating 1 and 2 will cause the loss of virtualzation functionality of
  the compute node, which may lead to data plane services interruption
  if the virtual resource is not redudant.
| Updating 3 might result the same.
| Updating 4 might lead to control plane services interruption if not an
  HA deployment.

**Networking node**

1. OS kernel, optional, not all switch/router allow you to upgrade its
   OS since it is more like a firmware than a generic OS.
2. User space software package, like neutron agents and other control
   plane programs

| Updating 1 if allowed will cause a node reboot and therefore leads to
  data plane services interruption if the virtual resource is not
  redudant.
| Updating 2 might lead to control plane services interruption if not an
  HA deployment.

**Storage node**

1. OS kernel, optional, not all storage node allow you to upgrade its OS
   since it is more like a firmware than a generic OS.
2. Kernel modules
3. User space software packages, control plane programs

| Updating 1 if allowed will cause a node reboot and therefore leads to
  data plane services interruption if the virtual resource is not
  redudant.
| Update 2 might result in the same.
| Updating 3 might lead to control plane services interruption if not an
  HA deployment.

**Management node**

1. OS Kernel
2. Kernel modules, like driver
3. User space software packages, like database, message queue and
   control plane programs.

| Updating 1 will cause a node reboot and therefore leads to control
  plane services interruption if not an HA deployment. Updating 2 might
  result in the same.
| Updating 3 might lead to control plane services interruption if not an
  HA deployment.

Upgrade Span
~~~~~~~~~~~~

| **Major Upgrade**
| Upgrades between major releases may introducing significant changes in
  function, configuration and data, such as the upgrade of OPNFV from
  Arno to Brahmaputra.

| **Minor Upgrade**
| Upgrades inside one major releases which would not leads to changing
  the structure of the platform and may not infect the schema of the
  system data.

Upgrade Granularity
~~~~~~~~~~~~~~~~~~~

Physical/Hardware Dimension
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Support full / partial upgrade for data centre, cluster, zone. Because
of the upgrade of a data centre or a zone, it may be divided into
several batches. The upgrade of a cloud environment (cluster) may also
be partial. For example, in one cloud environment running a number of
VNFs, we may just try one of them to check the stability and
performance, before we upgrade all of them.

Software Dimension
^^^^^^^^^^^^^^^^^^

-  The upgrade of host OS or kernel may need a 'hot migration'
-  The upgrade of OpenStack’s components
    i.the one-shot upgrade of all components
    ii.the partial upgrade (or bugfix patch) which only affects some
   components (e.g., computing, storage, network, database, message
   queue, etc.)

| ==[MT] this section seems to overlap with 2.1.==
| I can see the following dimensions for the software

-  different software packages
-  different funtions - Considering that the target versions of all
   software are compatible the upgrade needs to ensure that any
   dependencies between SW and therefore packages are taken into account
   in the upgrade plan, i.e. no version mismatch occurs during the
   upgrade therefore dependencies are not broken
-  same function - This is an upgrade specific question if different
   versions can coexist in the system when a SW is being upgraded from
   one version to another. This is particularly important for stateful
   functions e.g. storage, networking, control services. The upgrade
   method must consider the compatibility of the redundant entities.

-  different versions of the same software package
-  major version changes - they may introduce incompatibilities. Even
   when there are backward compatibility requirements changes may cause
   issues at graceful rollback
-  minor version changes - they must not introduce incompatibility
   between versions, these should be primarily bug fixes, so live
   patches should be possible

-  different installations of the same software package
-  using different installation options - they may reflect different
   users with different needs so redundancy issues are less likely
   between installations of different options; but they could be the
   reflection of the heterogeneous system in which case they may provide
   redundancy for higher availability, i.e. deeper inspection is needed
-  using the same installation options - they often reflect that the are
   used by redundant entities across space

-  different distribution possibilities in space - same or different
   availability zones, multi-site, geo-redundancy

-  different entities running from the same installation of a software
   package
-  using different startup options - they may reflect different users so
   redundancy may not be an issues between them
-  using same startup options - they often reflect redundant
   entities====

Upgrade duration
~~~~~~~~~~~~~~~~

As the OPNFV end-users are primarily Telco operators, the network
services provided by the VNFs deployed on the NFVI should meet the
requirement of 'Carrier Grade'.

In telecommunication, a "carrier grade" or"carrier class" refers to a
system, or a hardware or software component that is extremely reliable,
well tested and proven in its capabilities. Carrier grade systems are
tested and engineered to meet or exceed "five nines" high availability
standards, and provide very fast fault recovery through redundancy
(normally less than 50 milliseconds). [from wikipedia.org]

"five nines" means working all the time in ONE YEAR except 5'15".

We have learnt that a well prepared upgrade of OpenStack needs 10
minutes. The major time slot in the outage time is used spent on
synchronizing the database. [from ' Ten minutes OpenStack Upgrade? Done!
' by Symantec]

This 10 minutes of downtime of OpenStack however did not impact the
users, i.e. the VMs running on the compute nodes. This was the outage of
the control plane only. On the other hand with respect to the
preparations this was a manually tailored upgrade specific to the
particular deployment and the versions of each OpenStack service.

The project targets to achieve a more generic methodology, which however
requires that the upgrade objects fulfill ceratin requirements. Since
this is only possible on the long run we target first upgrades from
version to version for the different VIM services.

**Questions:**

#. | Can we manage to upgrade OPNFV in only 5 minutes?
   | ==[MT] The first question is whether we have the same carrier grade
     requirement on the control plane as on the user plane. I.e. how
     much control plane outage we can/willing to tolerate?
   | In the above case probably if the database is only half of the size
     we can do the upgrade in 5 minutes, but is that good? It also means
     that if the database is twice as much then the outage is 20
     minutes.
   | For the user plane we should go for less as with two release yearly
     that means 10 minutes outage per year.==
   | ==[Malla] 10 minutes outage per year to the users? Plus, if we take
     control plane into the consideration, then total outage will be
     more than 10 minute in whole network, right?==
   | ==[MT] The control plane outage does not have to cause outage to
     the users, but it may of course depending on the size of the system
     as it's more likely that there's a failure that needs to be handled
     by the control plane.==

#. | Is it acceptable for end users ? Such as a planed service
     interruption will lasting more than ten minutes for software
     upgrade.
   | ==[MT] For user plane, no it's not acceptable in case of
     carrier-grade. The 5' 15" downtime should include unplanned and
     planned downtimes.==
   | ==[Malla] I go agree with Maria, it is not acceptable.==

#. | Will any VNFs still working well when VIM is down?
   | ==[MT] In case of OpenStack it seems yes. .:)==

The maximum duration of an upgrade
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The duration of an upgrade is related to and proportional with the
  scale and the complexity of the OPNFV platform as well as the
  granularity (in function and in space) of the upgrade.
| [Malla] Also, if is a partial upgrade like module upgrade, it depends
  also on the OPNFV modules and their tight connection entities as well.

The maximum duration of a roll back when an upgrade is failed 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The duration of a roll back is short than the corresponding upgrade. It
  depends on the duration of restore the software and configure data from
  pre-upgrade backup / snapshot.
| ==[MT] During the upgrade process two types of failure may happen:
|  In case we can recover from the failure by undoing the upgrade
  actions it is possible to roll back the already executed part of the
  upgrade in graceful manner introducing no more service outage than
  what was introduced during the upgrade. Such a graceful roll back
  requires typically the same amount of time as the executed portion of
  the upgrade and impose minimal state/data loss.==
| ==[MT] Requirement: It should be possible to roll back gracefully the
  failed upgrade of stateful services of the control plane.
|  In case we cannot recover from the failure by just undoing the
  upgrade actions, we have to restore the upgraded entities from their
  backed up state. In other terms the system falls back to an earlier
  state, which is typically a faster recovery procedure than graceful
  roll back and depending on the statefulness of the entities involved it
  may result in significant state/data loss.==
| **Two possible types of failures can happen during an upgrade**

#. We can recover from the failure that occurred in the upgrade process:
   In this case, a graceful rolling back of the executed part of the
   upgrade may be possible which would "undo" the executed part in a
   similar fashion. Thus, such a roll back introduces no more service
   outage during an upgrade than the executed part introduced. This
   process typically requires the same amount of time as the executed
   portion of the upgrade and impose minimal state/data loss.
#. We cannot recover from the failure that occurred in the upgrade
   process: In this case, the system needs to fall back to an earlier
   consistent state by reloading this backed-up state. This is typically
   a faster recovery procedure than the graceful roll back, but can cause
   state/data loss. The state/data loss usually depends on the
   statefulness of the entities whose state is restored from the backup.

The maximum duration of a VNF interruption (Service outage)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Since not the entire process of a smooth upgrade will affect the VNFs,
  the duration of the VNF interruption may be shorter than the duration
  of the upgrade. In some cases, the VNF running without the control
  from of the VIM is acceptable.
| ==[MT] Should require explicitly that the NFVI should be able to
  provide its services to the VNFs independent of the control plane?==
| ==[MT] Requirement: The upgrade of the control plane must not cause
  interruption of the NFVI services provided to the VNFs.==
| ==[MT] With respect to carrier-grade the yearly service outage of the
  VNF should not exceed 5' 15" regardless whether it is planned or
  unplanned outage. Considering the HA requirements TL-9000 requires an
  ent-to-end service recovery time of 15 seconds based on which the ETSI
  GS NFV-REL 001 V1.1.1 (2015-01) document defines three service
  availability levels (SAL). The proposed example service recovery times
  for these levels are:
| SAL1: 5-6 seconds
| SAL2: 10-15 seconds
| SAL3: 20-25 seconds==
| ==[Pva] my comment was actually that the downtime metrics of the
  underlying elements, components and services are small fraction of the
  total E2E service availability time. No-one on the E2E service path
  will get the whole downtime allocation (in this context it includes
  upgrade process related outages for the services provided by VIM etc.
  elements that are subject to upgrade process).==
| ==[MT] So what you are saying is that the upgrade of any entity
  (component, service) shouldn't cause even this much service
  interruption. This was the reason I brought these figures here as well
  that they are posing some kind of upper-upper boundary. Ideally the
  interruption is in the millisecond range i.e. no more than a
  switchover or a live migration.==
| ==[MT] Requirement: Any interruption caused to the VNF by the upgrade
  of the NFVI should be in the sub-second range.==

==[MT] In the future we also need to consider the upgrade of the NFVI,
i.e. HW, firmware, hypervisors, host OS etc.==