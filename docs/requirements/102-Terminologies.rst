===========
Terminology
===========

Terminologies
=============

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

Abbreviations
=============

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

