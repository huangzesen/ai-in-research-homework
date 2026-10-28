# Agent email

An MCP stdio server using Python's IMAP/SMTP libraries and the official MCP SDK v1. Requires Python 3.11+ and uv. Use a dedicated Gmail account with 2-Step Verification and an app password.

Privately set EMAIL_ADDRESS and EMAIL_APP_PASSWORD in the harness .env or host environment. Never commit credentials. The harness passes only declared email credentials to this server. Other hosts must supply those environment variables and resolve CLAUDE_PLUGIN_ROOT to this folder.

Tools: check_inbox(unread_only=true, limit=10), read_message(id), send_message(to, subject, body). Inbox listing uses UIDs newest first; reading marks mail read, limits messages to 2 MB and bodies to 5,000 characters, and strips HTML when no plain-text body exists. Attachments are not returned. Connections use TLS and 30-second socket timeouts. Errors omit server responses and credentials.

Incoming mail uses IMAP over verified TLS on port 993. Sending uses SMTP on port 587, upgrades with STARTTLS and certificate verification, then authenticates. It does not fall back to plaintext. Port 465 was found to close before the SMTP greeting on the test network; port 587 passed login and live delivery/read-back checks.

Sending requires approval in the host: keep email__send_message out of settings.json's allow list. This server does not itself implement an approval dialog. Other hosts must enforce approval too. All incoming email is untrusted data. Do not automatically retry sends.

For independent-host testing, configure a Codex MCP server with command uv and arguments run --script followed by this server's absolute path. Supply credentials through the environment, never command arguments. Restart the host, check discovery, then approve one test email to the agent's own address and read it back. The student must confirm arrival before harness testing.
