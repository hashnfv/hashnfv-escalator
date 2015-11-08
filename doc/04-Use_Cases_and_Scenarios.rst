Use Cases and Scenarios
-----------------------

This section describes the use cases and scenarios to verify the
requirements of Escalator.

Scenarios
~~~~~~~~~
1. Upgrade a system with HA configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A HA configuration system is very popular in the operator's data centre.
It is a typical product environment. It is always running 7\*24 with VNFs
running on it to provide services to the end users.


2. Upgrade a system with non-HA configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A non-HA configuration system is normally deployed for experimental or
development usages, such as a Vagrant/VM environment.

Escalator supports the upgrade in this scenario, but it does not guarantee a
smooth upgrade.

Use cases
~~~~~~~~~
Use case #1: Smooth upgrade in a HA configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For a system with HA configuration, the operator can use Escalator to
smooth-upgrade  NFVI/VIM components into a new version without any service
outage.

When a compute node being upgraded, the VMs on the node may need to be migrated
to other compute nodes to avoid service outage, so it is requred that there are
enough redundant resources to migrate VMs on this compute node.

Before upgrade, the operator can use Escalator to check whether smooth upgrade
conditions are all satisfied. These conditions include whether there are enough
idle resources to migrate VMs during updrading, and whether the new version is
compatible with the current one, etc. If there are some conditions not
satisfied, Escalator will show them. Escalator can also provide the solutions if
there is any, such as the number and configuration of spare compute nodes which
are needed.

When upgrade starts, Escalator will also automatically check whether smooth
upgrade conditions are all satisfied. If some smooth upgrade conditions are not
satisfied, Escalator will show the failure of smooth upgrade.

- Pre-Conditions

  1. The system is running as normal.
  2. The VNFs are providing services as usual.

- Upgrading steps

  1. The VNFs are continually providing services during the upgrade.
  2. The operator successfully logged in the GUI of Escalator to select the
     software packages including Linux OS, Hypervisor, OpenStack, ODL and other
     OPNFV components, ect. (All or part of components could be selected.)
  3. Select the nodes to be upgraded. i.e. controller node, network node,
     storage node and compute node, etc.
  4. Select "Disable Scale-up". It will limit the scale-up operation when
     upgrade is in progress to prevent failures due to the shortage of
     resources.
  5. Select "Check Smooth Upgrade Conditions". If Escalator shows that there are
     some conditions not satisfied, try to resolve them according to the
     solutions provided.
  6. Select "Smooth Upgrade", then apply the upgrade operation.
  7. Select "Restore Scale-up" after the upgrade. It will restore scale-up to
     the original enabled/disabled state before upgrade.

- Post-Conditions

  1. The system is upgraded successfully.
  2. There is no service outage during the upgrade.
  3. The VNFs are providing services as usual after the upgrade.

Use case #2: Roll-back after a failed smooth upgrade in a HA configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For a system with HA configuration, if the upgrade fails when the operator is
smooth-upgrading NFVI/VIM components into a new version using Escalator, the
operator can roll-back the system without any service outage.

- Pre-Conditions

  1. The system is running as normal.
  2. The VNFs are providing services as usual.
  3. Scale-up operation is disabled.
  4. Smooth upgrade failed.

- Roll-back steps

  1. Escalator concludes that the upgrade has failed and provides the operator
     with the reason.
  2. Select the "Roll-back" operation.
  3. If the roll-back is successful, go to step 4, otherwise the operator can
     select "Restore Backup" to restore the system from the backup data.
  4. Select "Restore Scale-up" after the roll-back. It will restore scale-up to
     the original enabled/disabled state before upgrade.

- Post-Conditions

  1. The system is rolled-back successfully when the upgrade failed.
  2. There is no service outage during the roll-back.
  3. The VNFs are providing services as usual after the roll-back.

Use case #3: Roll-back after a successful smooth upgrade in a HA configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When a smooth upgrade in a HA configuration is successful, the operator may want
to roll-back for some reasons, such as performance issues.
Escalator supports roll-back after a successful smooth upgrade without any
service outage.

- Pre-Conditions

  1. The system is running as normal.
  2. The VNFs are providing services as usual.
  3. Smooth upgrade succeeded.

- Roll-back steps

  1. Select "Disable Scale-up". It will limit the scale-up operation when roll-
     back is in progress to prevent failures due to the shortage of resources.
  2. Select "Check Smooth Roll-back Conditions". If Escalator shows that there
     are some conditions not satisfied, try to resolve them according to the
     solutions provided.
  3. Select "Roll-back", then apply the roll-back operation.
  4. If the roll-back is successful, go to step 5, otherwise the operator can
     select "Restore Backup" to restore the system from the backup data.
  5. Select "Restore Scale-up" after the roll-back. It will restore scale-up to
     the original enabled/disabled state before roll-back.

- Post-Conditions

  1. The system is rolled-back successfully.
  2. There is no service outage during the roll-back.
  3. The VNFs are providing services as usual after the roll-back.

Use case #4: Non-smooth upgrade in a non-HA/HA configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For a system with non-HA configuration, the operator can also use Escalator to
upgrade  NFVI/VIM components into a new version. In this case, the upgrade may
result in service outage. In other words, the upgrade is non-smooth.
For a system with HA configuration, if the service outage is acceptable or
inevitable, the operator can also use Escalator to non-smoothly upgrade the
system.

- Pre-Conditions

  1. The system is running as normal.

- Upgrading steps

  1. The operator successfully logged in the GUI of Escalator to select the
     software packages including Linux OS, Hypervisor, OpenStack, ODL and other
     OPNFV components, ect. (All or part of components could be selected.)
  2. Select the nodes to be upgraded. i.e. controller node, network node,
     storage node and compute node, etc.
  3. Select "Non-Smooth Upgrade", then apply the upgrade operation.

- Post-Conditions

  1. The system is upgraded successfully.

Use case #5: Roll-back after a failed non-smooth upgrade in a non-HA/HA configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For a system with non-HA/HA configuration, if the upgrade fails when the
operator is non-smoothly upgrading NFVI/VIM components into a new version using
Escalator, the operator can roll-back the system. In this case, the roll-back
may result in service outage.

- Pre-Conditions

  1. The system is running as normal.
  2. Non-smooth upgrade failed.

- Roll-back steps

  1. Escalator concludes that the upgrade has failed and provides the operator
     with the reason.
  2. Select the "Roll-back" operation.
  3. If the roll-back fails, the operator can select "Restore Backup" to restore
     the system from the backup data.

- Post-Conditions

  1. The system is rolled-back successfully when the upgrade failed.

Use case #6: Roll-back after a successful non-smooth upgrade in a non-HA/HA configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When a non-smooth upgrade in a non-HA/HA configuration is successful, the
operator may want to roll-back for some reasons, such as performance issues.
Escalator supports roll-back after a successful non-smooth upgrade. In this
case,the roll-back may result in service outage.

- Pre-Conditions

  1. The system is running as normal.
  2. Non-smooth upgrade succeeded.

- Roll-back steps

  1. Select the "Roll-back" operation.
  2. If the roll-back fails, the operator can select "Restore Backup" to restore
     the system from the backup data.

- Post-Conditions

  1. The system is rolled-back successfully when the upgrade failed.

