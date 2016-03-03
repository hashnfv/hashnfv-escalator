===========
Terminology
===========

Terminologies
=============

Backup
  The term refers to making a copy of the system persistent data to a storage,
  so that it can be used to restore the system or a given part of it to the same
  state as it was when the backup was created. Restoring from backup will lose
  volatile states like CPU and memory content. Changes made to the system from
  the moment the backup was created to the moment it is used to restore the
  (sub)system are also lost in the restoration process. 

Carrier Grade
  The refers to a system, or a hardware or software component that is extremely
  reliable, well tested and proven in its capabilities. Carrier grade systems are
  tested and engineered to meet or exceed "five nines" high availability standards,
  and provide very fast fault recovery through redundancy (normally less than 50 
  milliseconds). Sometimes, Carrier grade is also referred as Carrier Class.

Downgrade
  The term refers to an upgrade operation in which an earlier version of the
  software is restored through the upgrade procedure. Compared to rollback,
  Downgrade is normally initiated with Operator, and it is allowed to select any
  earlier version, providing the compatibility of the versions is met or upgrade
  strategies are allowed (whether service outage or data lost can be tolerant.)

End-User
  The term refers to a subscriber of the Operator's services.

High Availability(HA)
  High Availability refers to a system or component that is continuously
  operational for a desirably long length of time even a part of it is out of
  service. Carrier Grade Availability is a typical HA example. HA system is popular
  in Operator's data center for critical tasks. Non-HA system is normally deployed
  for experimental or in-critical tasks in favor of its simplicity.

Infrastructure Services
  The term refers to services provided by the NFV Infrastructure to the VNFs
  as required by the Management & Orchestration functions and especially the VIM.
  I.e. these are the virtual resources as perceived by the VNFs.

Infrastructure Resource Model
  The term refers to the representation of infrastructure resources,
  namely: the physical resources, the virtualization
  facility resources and the virtual resources.

Network Service
  The term refers to a service provided by an Operator to its
  end-users using a set of (virtualized) Network Functions

Operator
  The term refers to network service providers and Virtual Network
  Function (VNF) providers.

Outage
  The terms refers to the period of time when a given service is not available
  to End-Users.

Parallel Universe Upgrade
  The term refers to an upgrade strategy, which creates and deploys
  a new universe - a system with the new configuration - while the old
  system continues running. The state of the old system is transferred
  to the new system after sufficient testing of the new system.

Physical Resource
  The term refers to a piece of hardware in the NFV infrastructure that may
  also include firmware enabling this piece of hardware.

Restore
  The term refers to a failure handling strategy that reverts the changes
  done, for example, by an upgrade by restoring the system from some backup
  data. This results in the loss of any change and data persisted after the
  backup was been taken. To recover those additional measures need to be taken
  if necessary (e.g. Rollforward).

Rollback
  The term refers to a failure handling strategy that reverts the changes
  done by a potentially failed upgrade execution one by one in a reverse order.
  I.e. it is like undoing the changes done by the upgrade.

Rollforward
  The term refers to a failure handling strategy applied after a restore
  (from a backup) operation to recover any loss of data persisted between
  the time the backup has been taken and the moment it is restored. Rollforward
  requires that data that needs to survive the restore operation is logged at
  a location not impacted by the restore so that it can be re-applied to the
  system after its restoration from the backup.

Rolling Upgrade
  The term refers to an upgrade strategy, which upgrades a node or a subset
  of nodes at a time in a wave style rolling through the data centre. It
  is a popular upgrade strategy to maintain service availability.

Smooth Upgrade
  The term refers to an upgrade that results in no service outage
  for the end-users.

Snapshot
  The term refer to the state of a system at a particular point in time, or
  the action of capturing such a state.

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
  service availability.

Virtualization Facility
  The term refers to a resource that enables the creation
  of virtual environments on top of the physical resources, e.g.
  hypervisor, OpenStack, etc.

Virtual Resource
  The term refers to a resource, which is provided as services built on top
  of the physical resources via the virtualization facilities; in particular,
  virtual resources are the resources on which VNFs are deployed. Examples of
  virtual resources are: VMs, virtual switches, virtual routers, virtual disks.

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
