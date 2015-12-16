============
Requirements
============

Upgrade duration
================

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Pre-upgrading Environment
=========================

System is running normally. If there are any faults before the upgrade,
it is difficult to distinguish between upgrade introduced and the environment
itself.

The environment should have the redundant resources. Because the upgrade
process is based on the business migration, in the absence of resource
redundancy,it is impossible to realize the business migration, as well as to
achieve a smooth upgrade.

Resource redundancy in two levels:

NFVI level: This level is mainly the compute nodes resource redundancy.
During the upgrade, the virtual machine on business can be migrated to another
free compute node.

VNF level: This level depends on HA mechanism in VNF, such as:
active-standby, load balance. In this case, as long as business of the target
node on VMs is migrated to other free nodes, the migration of VM might not be
necessary.

The way of redundancy to be used is subject to the specific environment.
Generally speaking, During the upgrade, the VNF's service level availability
mechanism should be used in higher priority than the NFVI's. This will help
us to reduce the service outage.

Release version of software components
======================================

This is primarily a compatibility requirement. You can refer to Linux/Python
Compatible Semantic Versioning 3.0.0:

Given a version number MAJOR.MINOR.PATCH, increment the:

MAJOR version when you make incompatible API changes,

MINOR version when you add functionality in a backwards-compatible manner,

PATCH version when you make backwards-compatible bug fixes.

Some internal interfaces of OpenStack will be used by Escalator indirectly,
such as VM migration related interface between VIM and NFVI. So it is required
to be backward compatible on these interfaces. Refer to "Interface" chapter
for details.

Work Flows
==========

Describes the different types of requirements.  To have a table to label the source of
the requirements, e.g. Doctor, Multi-site, etc.

Basic Actions
=============

This section describes the basic functions may required by Escalator.

Preparation (offline)
^^^^^^^^^^^^^^^^^^^^^

This is the design phase when the upgrade plan (or upgrade campaign) is
being designed so that it can be executed automatically with minimal
service outage. It may include the following work:

1. Check the dependencies of the software modules and their impact,
   backward compatibilities to figure out the appropriate upgrade method
   and ordering.
2. Find out if a rolling upgrade could be planned with several rolling
   steps to avoid any service outage due to the upgrade some
   parts/services at the same time.
3. Collect the proper version files and check the integration for
   upgrading.
4. The preparation step should produce an output (i.e. upgrade
   campaign/plan), which is executable automatically in an NFV Framework
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

.. <hujie> Depends on the attributes of the object being upgraded, the
  upgrade plan may be slitted into step(s) and/or sub-plan(s), and even
  more small sub-plans in design phase. The plan(s) or sub-plan(s) my
  include step(s) or sub-plan(s).

Validation the upgrade plan / Checking the pre-requisites of System( offline / online)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The upgrade plan should be validated before the execution by testing
it in a test environment which is similar to the product environment.

.. <MT> However it could also mean that we can identify some properties
  that it should satisfy e.g. what operations can or cannot be executed
  simultaneously like never take out two VMs of the same VNF.

.. <MT> Another question is if it requires that the system is in a particular
  state when the upgrade is applied. I.e. if there's certain amount of
  redundancy in the system, migration is enabled for VMs, when the NFVI
  is upgraded the VIM is healthy, when the VIM is upgraded the NFVI is
  healthy, etc.

.. <MT> I'm not sure what online validation means: Is it the validation of the
  upgrade plan/campaign or the validation of the system that it is in a
  state that the upgrade can be performed without too much risk?==

Before the upgrade plan being executed, the system healthy of the
online product environment should be checked and confirmed to satisfy
the requirements which were described in the upgrade plan. The
sysinfo, e.g. which included system alarms, performance statistics and
diagnostic logs, will be collected and analogized. It is required to
resolve all of the system faults or exclude the unhealthy part before
executing the upgrade plan.


Backup/Snapshot (online)
^^^^^^^^^^^^^^^^^^^^^^^^

For avoid loss of data when a unsuccessful upgrade was encountered, the
data should be back-upped and the system state snapshot should be taken
before the execution of upgrade plan. This would be considered in the
upgrade plan.

Several backups/Snapshots may be generated and stored before the single
steps of changes. The following data/files are required to be
considered:

1. running version files for each node.
2. system components' configuration file and database.
3. image and storage, if it is necessary.

.. <MT> Does 3 imply VNF image and storage? I.e. VNF state and data?==

.. <hujie> The following text is derived from previous "4. Negotiate
  with the VNF if it's ready for the upgrade"

Although the upper layer, which include VNFs and VNFMs, is out of the
scope of Escalator, but it is still recommended to let it ready for a
smooth system upgrade. The escalator could not guarantee the safe of
VNFs. The upper layer should have some safe guard mechanism in design,
and ready for avoiding failure in system upgrade.

Execution (online)
^^^^^^^^^^^^^^^^^^

The execution of upgrade plan should be a dynamical procedure which is
  controlled by Escalator.

.. <hujie> Revised text to be general.==

1. It is required to supporting execution ether in sequence or in
   parallel.
2. It is required to check the result of the execution and take the
   action according the situation and the policies in the upgrade plan.
3. It is required to execute properly on various configurations of
   system object. I.e. stand-alone, HA, etc.
4. It is required to execute on the designated different parts of the
   system. I.e. physical server, virtualized server, rack, chassis,
   cluster, even different geographical places.

Testing (online)
^^^^^^^^^^^^^^^^

The testing after upgrade the whole system or parts of system to make
sure the upgraded system(object) is working normally.

.. <hujie> Revised text to be general.

1. It is recommended to run the prepared test cases to see if the
   functionalities are available without any problem.
2. It is recommended to check the sysinfo, e.g. system alarms,
   performance statistics and diagnostic logs to see if there are any
   abnormal.

Restore/Roll-back (online)
^^^^^^^^^^^^^^^^^^^^^^^^^^

When upgrade is failure unfortunately, a quick system restore or system
roll-back should be taken to recovery the system and the services.

.. <hujie> Revised text to be general.

1. It is recommend to support system restore from backup when upgrade
   was failed.
2. It is recommend to support graceful roll-back with reverse order
   steps if possible.

Monitoring (online)
^^^^^^^^^^^^^^^^^^^

Escalator should continually monitor the process of upgrade. It is
keeping update status of each module, each node, each cluster into a
status table during upgrade.

.. <hujie> Revised text to be general.

1. It is required to collect the status of every objects being upgraded
   and sending abnormal alarms during the upgrade.
2. It is recommend to reuse the existing monitoring system, like alarm.
3. It is recommend to support pro-actively query.
4. It is recommend to support passively wait for notification.

**Two possible ways for monitoring:**

**Pro-Actively Query** requires NFVI/VIM provides proper API or CLI
interface. If Escalator serves as a service, it should pass on these
interfaces.

**Passively Wait for Notification** requires Escalator provides
callback interface, which could be used by NFVI/VIM systems or upgrade
agent to send back notification.

.. <hujie> I am not sure why not to subscribe the notification.

Logging (online)
^^^^^^^^^^^^^^^^

Record the information generated by escalator into log files. The log
file is used for manual diagnostic of exceptions.

1. It is required to support logging.
2. It is recommended to include time stamp, object id, action name,
   error code, etc.

Administrative Control (online)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Administrative Control is used for control the privilege to start any
escalator's actions for avoiding unauthorized operations.

#. It is required to support administrative control mechanism
#. It is recommend to reuse the system's own secure system.
#. It is required to avoid conflicts when the system's own secure system
   being upgraded.

Requirements on Object being upgraded
=====================================

.. <hujie> We can develop BPs in future from requirements of this section and
  gap analysis for upper stream projects

Escalator focus on smooth upgrade. In practical implementation, it
might be combined with installer/deplorer, or act as an independent
tool/service. In either way, it requires targeting systems(NFVI and
VIM) are developed/deployed in a way that Escalator could perform
upgrade on them.

On NFVI system, live-migration is likely used to maintain availability
because OPNFV would like to make HA transparent from end user. This
requires VIM system being able to put compute node into maintenance mode
and then isolated from normal service. Otherwise, new NFVI instances
might risk at being schedule into the upgrading node.

On VIM system, availability is likely achieved by redundancy. This
impose less requirements on system/services being upgrade (see PVA
comments in early version). However, there should be a way to put the
target system into standby mode. Because starting upgrade on the
master node in a cluster is likely a bad idea.

.. <hujie>Revised text to be general.

1. It is required for NFVI/VIM to support **service handover** mechanism
   that minimize interruption to 0.001%(i.e. 99.999% service
   availability). Possible implementations are live-migration, redundant
   deployment, etc, (Note: for VIM, interruption could be less
   restrictive)

2. It is required for NFVI/VIM to restore the early version in a efficient
   way, such as **snapshot**.

3. It is required for NFVI/VIM to **migration data** efficiently between
   base and upgraded system.

4. It is recommend for NFV/VIM's interface to support upgrade
   orchestration, e.g. reading/setting system state.

Functional Requirements
=======================

Availability mechanism, etc.

Non-functional Requirements
===========================
