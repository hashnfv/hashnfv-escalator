Requirements from other OPNFV projects
--------------------------------------

| We have created a questionnaire for collecting other projects
  requirments
  (https://docs.google.com/forms/d/11o1mt15zcq0WBtXYK0n6lKF8XuIzQTwvv8ePTjmcoF0/viewform?usp=send_form),
  please advertise it.
| ==[hujie] Can we force other OPNFV projects to complete the survey by
  using JIRA dependence?==

Doctor Project
~~~~~~~~~~~~~~

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

HA Project
~~~~~~~~~~

Multi-site Project
~~~~~~~~~~~~~~~~~~

-  Escalator upgrade one site should at least not lead to the other site
   API token validation failed.
