# Week 5 graceful conversation recovery

Evidence: student report in the homework session.

The student asked the agent to remember CRASH-482 in conversation only, without writing files or using tools. After stopping the agent and starting it again, they asked for the tag. The reported reply was: "The recovery tag you gave me for this conversation is CRASH-482."

This confirms remembered conversation content across a manual restart. It is a graceful-restart test, not the separate forced-crash/tool interruption or uncertain SMTP-delivery demonstration.
