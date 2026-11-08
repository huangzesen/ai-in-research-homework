# macOS launchd service

The plist is a privacy-sanitized export of the tested service. Replace /Users/AGENT_USER, including HOME, project, venv, log and certifi paths, before installation. The running Mac uses real absolute paths. Generate its local plist with `.venv/bin/python service_control.py generate`, then install with `install`; use `status`, `stop`, `start` for control. No credentials are embedded.

RunAtLoad and KeepAlive, 10-second throttling, private logs and caffeinate -i -s. Keep AC connected, lid open, user logged in. Telegram /stop cancels work; it does not unload launchd. Automatic SIGKILL restart was observed in 11.391 seconds. No actual logout/login test is claimed.
