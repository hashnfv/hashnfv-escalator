============
Requirements
============

Upgrade duration
================

Being a telecom service system, OPNFV shall target at carrier grade availability,
which allows only about 5 minutes of outage in a year. Base on this basic input
and discussions on the current solutions, The following requirements are defined
from the perspective of time constraints:

- OPNFV platform must be deployed with HA to allow live upgrade possible. Considering of
  the scale, complexity, and life cycle of OPNFV system, allocating less than
  5 minutes out of a year for upgrade is in-realistic. Therefore OPNFV should
  be deployed with HA, allowing part of system being upgraded, while its
  redundant parts continue to serve End-User. This hopefully relieves the time
  constraint on upgrade operation to achievable level.

- VNF service interruption for each switching should be sub-second range. In
  HA system, switching from an in-service system/component to the redundant
  ones normally cause service interruption. From example live-migrating a
  virtual machine from one hypervisor to another typically take the virtual
  machine out of service for about 500ms. Summing up all these interruptions in
  a year shall be less than 5 minutes in order to fulfill the five-nines carrier
  grade availability. In addition, when interruption goes over a second, End-User
  experience is likely impacted. This document therefore recommends service
  switching should be less than a second.

- VIM interruption shall not result in NFVI interruption. VIM in general has more
  logic built-in, therefore more complicated, and likely less reliable than NFVI.
  To minimize the impact from VIM to NFVI, unless VIM explicitly order NFVI stop
  functioning, NFVI shall continue working as it should.

- Total upgrade duration should be less than 2 hours. Even time constraint is
  relieved with HA design, the total time for upgrade operation is recommended
  to limit in 2 hours. The reason is that upgrade might interfere End-User
  unexpectedly, shorter maintenance window is less possible risk. In this
  document, upgrade duration is started at the moment that End-User services
  are possibly impacted to the moment that upgrade is concluded with either
  commit or rollback. Regarding on the scale and complexity of OPNFV system,
  this requirements looks challenging, however OPNFV implementations should
  target this with introducing novel designs and solutions.

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
