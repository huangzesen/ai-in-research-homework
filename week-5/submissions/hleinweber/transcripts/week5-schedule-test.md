# Week 5 step 2: live schedule check

Evidence: student report during the homework session.

- A scheduled job automatically produced the Telegram response: "Scheduled wake-up received. Do not use tools."
- The bot confirmed removal of schedule-demo.
- A later explicit list request showed only morning-papers, running at 08:00 Monday through Friday.
- The model copied the instruction "Do not use tools" into its response. The demo task wording has since been clarified; an exact-output rerun has not been done.
- The first attempt to request the job list used Telegram Reply and was silently ignored by the original approval-reply filter. A new message worked. Step 3 changes routing to accept ordinary replies while discarding replies to saved approval prompts.

This is a functional scheduling check, not an overnight run.
