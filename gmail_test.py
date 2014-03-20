import os
import email
import imaplib

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(os.environ["GMAIL_ACCOUNT"], os.environ["GMAIL_PASSWORD"])
mail.select("inbox")

MAX_LINES = 5

#  Retrieve ids of all emails
rv, data = mail.search(None, "ALL")

#  This script retrieves the email body, marking it as read. Store ids of unread emails
rv, unread = mail.search(None, "UNSEEN")
unread_ids = unread[0].decode("ascii").split(" ")

#  Only view 4 most recent emails
for num in data[0].split()[:-5:-1]:
	resp, msg_data = mail.fetch(num, "(RFC822)")
	msg = email.message_from_string(msg_data[0][1].decode("ascii"))
	print("---------------------------------------------------------")
	print(" {0}; From {1}\n {2}".format(num.decode("ascii"), msg["from"], msg["subject"]))
	body = msg.get_payload()

	#  If email was unread prior to receiving message payload, mark as unread
	if num.strip() in unread_ids:
		mail.store(num, "FLAGS", "UNSEEN")
		print(" ******NEW MESSAGE******")
	print("---------------------------------------------------------") 
	if type(body) is list:
		body_text = body[0].as_string()
	else:
		body_text = str(body)
	body_lines = body_text.split("\n")
	body_lines = [x for x in body_lines if not x.startswith("Content") and not x.strip() == ""]
	if len(body_lines) > (MAX_LINES):
		print("\t"+ "\n\t".join(body_lines[:MAX_LINES]))
	else:
		print("\t" + "\n\t".join(body_lines))
	print("")
