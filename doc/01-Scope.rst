Scope
-----

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