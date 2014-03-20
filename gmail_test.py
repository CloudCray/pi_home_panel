import os
import email
import imaplib

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(os.environ["GMAIL_ACCOUNT"], os.environ["GMAIL_PASSWORD"])
mail.select("inbox")

MAX_LINES = 5

rv, data = mail.search(None, "ALL")
for num in data[0].split()[:-5:-1]:
	resp, msg_data = mail.fetch(num, "(RFC822)")
	msg = email.message_from_string(msg_data[0][1].decode("ascii"))
	print("-----------------------------------------------")
	print("\t{0}; From {1}\n\t{2}".format(num.decode("ascii"), msg["from"], msg["subject"]))
	print("-----------------------------------------------")
	body = msg.get_payload()
	if type(body) is list:
		body_text = body[0].as_string()
	else:
		body_text = str(body)
	body_lines = body_text.split("\n")
	body_lines = [x for x in body_lines if not x.startswith("Content") and not x.strip() == ""]
	if len(body_lines) > (MAX_LINES):
		print("\n".join(body_lines[:MAX_LINES]))
	else:
		print(body_text)
