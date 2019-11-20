from UDPSocket import Client

PREFIX_LAD = "LAD"
PREFIX_USR = "USR"
 
# Database file
DATABASE   = "sysc3010.db"
ENCODING   = "utf-8"

BRANCH     = "Branches"
OBJECT     = "Ojects"

# Codes for sending and receiving
UPDATE     = "update|"
INSERT	   = "insert|"
DELETE     = "delete|"
CONTINUE   = "continue|"
EOF        = "***|"

def decode(message):
	message = message.replace(")(","|")
	message = message.strip("()")
	message_list = message.split("|")
	data_lists = list()

	for idx in range(len(message_list)):
		data_lists.append(message_list[idx].split(", "))

	return data_lists

if __name__ == "__main__":
	c = Client("127.0.0.1", 1001, "utf-8")
	while (True):
		msg = input("Enter Message: ")
		print(msg)
		c.send(msg)
		if msg == "***":
			break
	c.close()
	exit(0)
