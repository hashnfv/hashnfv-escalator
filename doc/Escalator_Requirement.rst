Draft Escalator Requirement v0.4
================================

Authors:
--------

| Jie Hu (ZTE, hu.jie@zte.com.cn)
| Qiao Fu (China Mobile, fuqiao@chinamobile.com)
| Ulrich Kleber (Huawei, Ulrich.Kleber@huawei.com)
| Maria Toeroe (Ericsson, maria.toeroe@ericsson.com)
| Sama, Malla Reddy (DOCOMO, sama@docomolab-euro.com)
| Zhong Chao (ZTE, chao.zhong@zte.com.cn)
| Julien Zhang (ZTE, zhang.jun3g@zte.com.cn)
| Yuri Yuan (ZTE, yuan.yue@zte.com.cn)
| Zhipeng Huang (Huawei, huangzhipeng@huawei.com)
| Jia Meng (ZTE, meng.jia@zte.com.cn)
| Liyi Meng (Ericsson, liyi.meng@ericsson.com)
| Pasi Vaananen (Stratus, pasi.vaananen@stratus.com)

1. Scope
--------

| This document describes the user requirements on the smooth upgrade
  function of the NFVI and VIM with respect to the upgrades of the OPNFV
  platform from one version to another. Smooth upgrade means that the
  upgrade results in no service outage for the end-users. This requires
  that the process of the upgrade is automatically carried out by a tool
  (code name: Escalator) with pre-configured data. The upgrade process
  includes preparation, validation, execution, monitoring and
  conclusion.
| ==[MT] While it is good to have a tool for the entire upgrade process,
  but it is a challenging task, so maybe we shouldn't require automation
  for the entire process right away. Automation is essential at
  execution.==
| ==[hujie] Maybe we can analysis information flows of the upgrade tool,
  abstract the basic / essential actions from the tool (or tools), and
  map them to a command set of NFVI / VIM's interfaces.==

The requirements are defined in a stepwise approach, i.e. in the first
phase focusing on the upgrade of the VIM then widening the scope to the
NFVI.

The requirements may apply to different NFV functions (NFVI, or VIM, or
both of them) . They will be classified in the Appendix of this
document.

2. General Requirements Background and terminology
--------------------------------------------------

==[MT] At the moment 2.1-2.3 seem to be more background sections than
requirements. Should we rename this part?==

2.1 Terminologies and definitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

2.2 Upgrade Objects
~~~~~~~~~~~~~~~~~~~

2.2.1 Physical Resource
^^^^^^^^^^^^^^^^^^^^^^^

| Most of the cloud infrastructures support dynamic addition/removal of
  hardware. A hardware upgrade could be done by removing the old
  hardware node and adding the new one. This will not be in the scope of
  this project.
| ==[MT] Does this mean that we are excluding firmware upgrades too?==

2.2.2 Virtual Resources
^^^^^^^^^^^^^^^^^^^^^^^

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

2.2.3 Virtualization Facility Resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Based on the functionality they provide, virtualization facility
  resources could be divided into computing node, networking node,
  storage node and management node.
| The possible upgrade objects in these nodes are addressed below:
  (Note: hardware based virtualization may considered as virtualization
  facility resource, but from escalator perspective, it is better
  considered it as part of hardware upgrade. )

**Computing node**

#. OS Kernel
#. Hypvervisor and virtual switch
#. Other kernel modules, like driver
#. User space software packages, like nova-compute agents and other
   control plane programs

| Updating 1 and 2 will cause the loss of virtualzation functionality of
  the compute node, which may lead to data plane services interruption
  if the virtual resource is not redudant.
| Updating 3 might result the same.
| Updating 4 might lead to control plane services interruption if not an
  HA deployment.

**Networking node**

#. OS kernel, optional, not all switch/router allow you to upgrade its
   OS since it is more like a firmware than a generic OS.
#. User space software package, like neutron agents and other control
   plane programs

| Updating 1 if allowed will cause a node reboot and therefore leads to
  data plane services interruption if the virtual resource is not
  redudant.
| Updating 2 might lead to control plane services interruption if not an
  HA deployment.

**Storage node**

#. OS kernel, optional, not all storage node allow you to upgrade its OS
   since it is more like a firmware than a generic OS.
#. Kernel modules
#. User space software packages, control plane programs

| Updating 1 if allowed will cause a node reboot and therefore leads to
  data plane services interruption if the virtual resource is not
  redudant.
| Update 2 might result in the same.
| Updating 3 might lead to control plane services interruption if not an
  HA deployment.

**Management node**

#. OS Kernel
#. Kernel modules, like driver
#. User space software packages, like database, message queue and
   control plane programs.

| Updating 1 will cause a node reboot and therefore leads to control
  plane services interruption if not an HA deployment. Updating 2 might
  result in the same.
| Updating 3 might lead to control plane services interruption if not an
  HA deployment.

2.3 Upgrade Span
~~~~~~~~~~~~~~~~

| **Major Upgrade**
| Upgrades between major releases may introducing significent changes in
  function, configuration and data, such as the upgrade of OPNFV from
  Arno to Brahmaputra.

| **Minor Upgrade**
| Upgrades inside one major releases which would not leads to changing
  the stucture of the platform and may not infect the schema of the
  system data.

2.4 Upgrade Granularity
~~~~~~~~~~~~~~~~~~~~~~~

2.4.1 Physical/Hardware Dimension
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Support full / partial upgrade for data centre, cluster, zone. Because
of the upgrade of a data centre or a zone, it may be divided into
several batches. The upgrade of a cloud environment (cluster) may also
be partial. For example, in one cloud environment running a number of
VNFs, we may just try one of them to check the stability and
performance, before we upgrade all of them.

2.4.2 Software Dimension
^^^^^^^^^^^^^^^^^^^^^^^^

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

3.5 Upgrade duration
~~~~~~~~~~~~~~~~~~~~

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

2.5.1 The maximum duration of an upgrade
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The duration of an upgrade is related to and proportional with the
  scale and the complexity of the OPNFV platform as well as the
  granularity (in function and in space) of the upgrade.
| [Malla] Also, if is a partial upgrade like module upgrade, it depends
  also on the OPNFV modules and their tight connection entites as well.

2.5.2 The maximum duration of a rollback when an upgrade is failed - this should be about rollback duration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The duration of a rollback is short than the corresponding upgrade. It
  depends on the duration of restore the software and configue data from
  pre-upgrade backup / snapshot.
| ==[MT] During the upgrade process two types of failure may happen:
|  In case we can recover from the failure by undoing the upgrade
  actions it is possible to roll back the already executed part of the
  upgrade in graceful manner introducing no more service outage than
  what was introduced during the upgrade. Such a graceful rollback
  requires typically the same amount of time as the executed portion of
  the upgrade and impose minimal state/data loss.==
| ==[MT] Requirement: It should be possible to roll back gracefully the
  failed upgrade of stateful services of the control plane.
|  In case we cannot recover from the failure by just undoing the
  upgrade actions, we have to restore the upgraded entities from their
  backed up state. In other terms the system falls back to an earlier
  state, which is typically a faster recovery procedure than graceful
  rollback and depending on the statefulness of the entities involved it
  may result in significant state/data loss.==
| **Two possible types of failures can happen during an upgrade**

#. We can recover from the failure that occured in the upgrade process:
   In this case, a graceful rolling back of the executed part of the
   upgrade may be possible which would "undo" the executed part in a
   similar fashion. Thus, such a roll back introduces no more service
   outage during an upgrade than the executed part introduced. This
   process typically requires the same amount of time as the executed
   portion of the upgrade and impose minimal state/data loss.
#. We cannot recover from the failure that occured in the upgrade
   process: In this case, the system needs to fall back to an earlier
   consistent state by reloading this backed-up state. This is typically
   a faster recovery procedure than the graceful rollback, but can cause
   state/data loss. The state/data loss usually depends on the
   statefulness of the entities whose state is restored from the backup.

2.5.3 The maximum duration of a VNF interruption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

3. Functional Considerations
----------------------------

3.1 Requirement of Escalator's Basic Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section describes the basic functions may required by Escalator.

3.1.1 Preparation (offline)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the design phase when the upgrade plan (or upgrade campaign) is
being designed so that it can be executed automatically with minimal
service outage. It may include the following work:

#. Check the dependencies of the software modules and their impact,
   backward compatibilities to figure out the appropriate upgrade method
   and ordering.
#. Find out if a rolling upgrade could be planned with several rolling
   steps to avoid any service outage due to the upgrade some
   parts/services at the same time.
#. Collect the proper version files and check the integration for
   upgrading.
#. The preparation step should produce an output (i.e. upgrade
   campaign/plan), which is executable automatically in an NFV Famawork
   and which can be validated before execution.

   -  The upgrade campaign should not be referring to scalable entities
      directly, but allow for adaptation to the system configuration and
      state at any given moment.
   -  The upgrade campaign should describe the ordering of the upgrade
      of different entities so that dependencies, redundancies can be
      maintained during the upgrade execution
   -  The upgrade campaign should provide information about the
      applicable recovery procedures and their ordering.
   -  The upgrade campaign should consider information about the
      verification/testing procedures to be performed during the upgrade
      so that upgrade failures can be detected as soon as possible and
      the appropriate recovery procedure can be identified and applied.
   -  The upgrade campaign should provide information on the expected
      execution time so that hanging execution can be identified
   -  The upgrade campaign should indicate any point in the upgrade when
      coordination with the users (VNFs) is required.

==[hujie]Depends on the attributes of the object being upgraded, the
upgrade plan may be slitted into step(s) and/or sub-plan(s), and even
more small sub-plans in design phase. The plan(s) or sub-plan(s) my
include step(s) or sub-plan(s).==

3.1.2 Validation the upgrade plan / Checking the pre-requisites of System( offline / online)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The upgrade plan should be validated before the execution by testing
  it in a test environment which is similar to the product environment.
| ==[MT]However it could also mean that we can identify some properties
  that it should satisfy e.g. what operations can or cannot be executed
  simultaneously like never take out two VMs of the same VNF.
| Another question is if it requires that the system is in a particular
  state when the upgrade is applied. I.e. if there's certain amount of
  redundacy in the system, migration is enabled for VMs, when the NFVI
  is upgraded the VIM is healthy, when the VIM is upgraded the NFVI is
  healthy, etc.
| I'm not sure what online validation means: Is it the validation of the
  upgrade plan/campaign or the validation of the system that it is in a
  state that the upgrade can be performed without too much risk?==

| Before the upgrade plan being executed, the system heathly of the
  online product environment should be checked and confirmed to satisfy
  the requirements which were described in the upgrade plan. The
  sysinfo, e.g. which included system alarms, performance statistics and
  diagnostic logs, will be collected and analyized. It is required to
  resolve all of the system faults or exclud the unhealthy part before
  executing the upgrade plan.
| ==[hujie] Text merged.==

3.1.3 Backup/Snapshot (online)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For avoid loss of data when a unsuccessful upgrade was encountered, the
data should be backuped and the system state snapshot should be taken
before the excution of upgrade plan. This would be considered in the
upgrade plan.

Several backups/Snapshots may be generated and stored before the single
steps of changes. The following data/files are required to be
considered:

#. running version files for each node.
#. system components' configuration file and database.
#. image and storage, if it is necessary.
   ==[MT] Does 3 imply VNF image and storage? I.e. VNF state and data?==

| ==[hujie] The following text is derived from previous "4. Negotiate
  with the VNF if it's ready for the upgrade"==
| Although the upper layer, which include VNFs and VNFMs, is out of the
  scope of Escalator, but it is still recommended to let it ready for a
  smooth system upgrade. The escalator could not garanttee the safe of
  VNFs. The upper layer should have some safe guard mechanism in design,
  and ready for avoiding failure in system upgrade.

3.1.4 Execution (online)
^^^^^^^^^^^^^^^^^^^^^^^^

| The execution of upgrade plan should be a dynamical procedure which is
  controlled by Escalator.
| ==[hujie] Revised text to be general.==

#. It is required to supporting execution ether in sequence or in
   parallel.
#. It is required to checke the result of the execution and take the
   action according the situation and the policies in the upgrade plan.
#. It is required to execute properly on various configurations of
   system object. I.e. stand-alone, HA, etc.
#. It is required to excecute on the designated different parts of the
   system. I.e. physical server, virtualized server, rack, chassis,
   cluster, even different geographical places.

3.1.5 Testing (online)
^^^^^^^^^^^^^^^^^^^^^^

| The testing after upgrade the whole system or parts of system to make
  sure the upgraded system(object) is working normally.
| ==[hujie] Revised text to be general.==

#. It is recommended to run the prepared test cases to see if the
   functionalities are availiable without any problem.
#. It is recommended to check the sysinfo, e.g. system alarms,
   performance statistics and diagnostic logs to see if there are any
   abnormal.

3.1.6 Restore/Rollback (online)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| When upgrade is failure unfortunatly, a quick system restore or system
  rollback should be taken to recovery the system and the services.
| ==[hujie] Revised text to be general.==

#. It is recommend to support system restore from backup when upgrade
   was failed.
#. It is recommend to support gracefull rollback with reverse order
   steps if possible.

3.1.7 Monitoring (online)
^^^^^^^^^^^^^^^^^^^^^^^^^

| Escalator should continually monitor the process of upgrade. It is
  keeping update status of each module, each node, each cluster into a
  status table during upgrade.
| ==[hujie] Revised text to be general.==

#. It is required to collect the status of every objects being upgraded
   and sending abnormal alerms during the upgrade.
#. It is recommend to reuse the existing monitoring system, like alarm.
#. It is recommend to support pro-actively query.
#. It is recommend to support passively wait for notification.

| **Two possible ways for monitoring:**
| **Pro-Actively Query** requires NFVI/VIM provides proper API or CLI
  interface. If Escalator serves as a service, it should pass on these
  interfaces.
| **Passively Wait for Notification** requires Escalator provides
  callback interface, which could be used by NFVI/VIM systems or upgrade
  agent to send back notification.
| [hujie] I am not sure why not to subscribe the notification.

3.1.8 Logging (online)
^^^^^^^^^^^^^^^^^^^^^^

Record the information generated by escalator into log files. The log
file is used for manual diagnostic of exceptions.

#. It is required to support logging.
#. It is recommended to include time stamp, object id, action name,
   error code, etc.

3.1.9 Administrative Control (online)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Administrative Control is used for control the privilege to start any
escalator's actions for avoding unauthorized operations.

#. It is required to support administrative control mechenism
#. It is recommed to reuse the system's own secure system.
#. It is required to avoid conflicts when the system's own secure system
   being upgraded.

3.2 Requirements on system object being upgraded
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| ==We can develope BPs in future from req of this section and GA for
  upper stream projects==
| Escalator focus on smooth upgrade. In practical implementation, it
  might be combined with installer/deployer, or act as an independent
  tool/service. In either way, it requires targeting systems(NFVI and
  VIM) are developed/deployed in a way that Escalator could perform
  upgrade on them.

On NFVI system, live-migration is likely used to maintain availability
because OPNFV would like to make HA transparent from end user. This
requires VIM system being able to put compute node into maintenance mode
and then isolated from normal service. Otherwise, new NFVI instances
might risk at being schedule into the upgrading node.

| On VIM system, availability is likely achieved by redundancy. This
  impose less requirements on system/services being upgrade (see PVA
  comments in early version). However, there should be a way to put the
  target system into standby mode. Because starting upgrade on the
  master node in a cluster is likely a bad idea.
| ==[hujie] Revised text to be general.==

#. It is required for NFVI/VIM to support **service handover** mechanism
   that minimize interruption to 0.001%(i.e. 99.999% service
   availability). Possible implementations are live-migration, redundant
   deployment, etc, (Note: for VIM, interruption could be less
   restrictive)
#. It is required for NFVI/VIM to restore the early verion in a efficent
   way, such as **snapshot**.
#. It is required for NFVI/VIM to **migration data** efficiently between
   base and upgraded system.
   ==[hujie] What is exact meaning of "base" here?==
#. It is recomend for NFV/VIM's interface to support upgrade
   orchestration, e.g. reading/setting system state
   ==[hujie] I am not sure if it reflect the previous text.==

4. Use Cases
------------

This section describes the use cases to verify the requirements of
Escalator.

4.1 Upgrade a system with minimal configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A minimal configuration system is normally depolyed for experimental or
developement ussage, such as a OPNFV test bed. Althouth it dose not have
large workload, but it is a typical system to be upgraded frequently.

4.2 Upgrade a system with HA configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A HA configuration system is very popular in the operator's data centre.
And it is a typical product environment. It always running 7 \* 24 a
week with VNFs running on it to provide services to the end users.

4.3 Upgrade a system with Multi-Site configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Upgrade in one site may cause service interruption to other site, if
both sites are depended and sharing the same modules/data base (e.g. a
keystone for both sites).

If a site failure during an upgrade, the rollback missing any minimal
state/data loss can cause an affect/failure to the depended site.

==Consider one site of ARNO release first. Then, multi-site in the
future.==

5. RA of Escalator
------------------

This section describes the reference architecture, the function blocks,
the function entities of Escalator for the reader to well understand how
the basic functions be organized.

6. Information Flows
--------------------

| This section describes the information flows among the function
  entities when Escalator is in actions.
| We should consider a generic procedure / frameworks of upgrading. And
  may provide a plugin interface for specialized tasks

7. Interfaces
-------------

This section describes the required interfaces of Escalator.

7.1 Manual Interface (CLI / GUI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

7.2 RESTful API
~~~~~~~~~~~~~~~

To support 3.3 Negotiate with the VNF if it's ready for the upgrade

7.3 Configuration File
~~~~~~~~~~~~~~~~~~~~~~

This section will suggest a format of the configuration files and how to
deal with it.

7.4 Log File
------------

This section will suggest a format of the log files and how to deal with
it.

8. Requirements from other OPNFV projects
-----------------------------------------

| We have created a questionnaire for collecting other projects
  requirments
  (https://docs.google.com/forms/d/11o1mt15zcq0WBtXYK0n6lKF8XuIzQTwvv8ePTjmcoF0/viewform?usp=send_form),
  please advertise it.
| ==[hujie] Can we force other OPNFV projects to complete the survey by
  using JIRA dependence?==

8.1 Doctor Project
~~~~~~~~~~~~~~~~~~

| ==Note: This scenario could be out of scope in Escalator project, but
  having the option to support this should be better to align with
  Doctor requirements.==
| The scope of Doctor project also covers maintenance scenario in which
  1) the VIM administorator requests host maintenance to VIM, 2) VIM
  will notifiy it to consumer such as VNFM to trigger application level
  migration or switching active-standby nodes, and 3) VIM waits responce
  from the consumer for a short while.

-  VIM should send out notification of VM migration to consumer (VNFM)
   as abstracted message like "maintenance".
-  VIM could wait VM migration until it receives "VM ready to
   maintenance" message from the owner (VNFM)

8.2 HA Project
~~~~~~~~~~~~~~

8.3 Multi-site Project
~~~~~~~~~~~~~~~~~~~~~~

-  Escalator upgrade one site should at least not lead to the other site
   API token validation failed.

9. Reference
------------

| [1] ETSI GS NFV 002 (V1.1.1): “Architectural Framework”
| [2] ETSI GS NFV 003 (V1.1.1): "Terminology for Main Concepts in NFV".
| [3] ETSI GS NFV-SWA001:“Virtual Network Function Architecture”
| [4] ETSI GS NFV-MAN001:“Management and Orchestration”
| [5] ETSI GS NFV-REL001:"Resiliency Requirements"
| [6] QuEST Forum TL-9000:"Quality Management System Requirement
  Handbook"
| [7] Service Availabilty Forum AIS:"Software Management Framework"

10. Useful Working Drafts of ETSI NFV
-------------------------------------

| Access them with your own ETSI account, please DO NOT disclose the
  content.
| [1] Migrate Virtualised Compute Resource operation @ 7.3.1.8
| ftp://docbox.etsi.org/ISG/NFV/Open/Drafts/IFA005_Or-Vi_ref_point_Spec/NFV-IFA005v070.zip
| [2] Reliability issues during NFV Software upgrade and improvement
  mechanisms @ 8
| ftp://@docbox.etsi.org/ISG/NFV/Open/Drafts/REL003_E2E_reliability_models/NFV-REL003v030.zip

Appendix
--------

A.1 Impact Analysis
~~~~~~~~~~~~~~~~~~~

Upgrading the different software modules may cause different impact on
the availability of the infrastracture resources and even on the service
continuity of the vNFs.

**Software modules in the computing nodes**

#. Host OS patch
   ==[MT] As SW module, we should list the host OS and maybe ====its
   drivers as well. From upgrade persepctive do we limit host OS
   upgrades to patches only?==
#. Hypervisor, such as KVM, QEMU, XEN, libvirt
#. Openstack agent in computing nodes (like Nova agent, Ceilometer
   agent...)

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

| These values provided come from internal testing and based on some
  assumptions, they may vary depending on the deployment techniques.
  Please feel free to add if you find more efficient values during your
  testing.
| https://wiki.opnfv.org/_media/upgrade_analysis_v0.5.xlsx
| Note that no redundancy of the software modules is considered in the
  table.
