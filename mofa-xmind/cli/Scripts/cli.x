args = get_args()
def PrintUsage():
	print("xmcli --updatekey or -uk key_name value")
	print("xmcli --getkey or -gk key_name")
	print("xmcli --deletekey or -dk key_name")

if args.size() <= 2:
	PrintUsage()
	return

# print("Connect to xMind thru 'lrpc:99023'")
import xMind thru 'lrpc:99023'
# print("Connected to xMind")

# Firt one is prog name
firstArg = args[1]
if (firstArg == "-uk" or firstArg == "--updatekey") and args.size()>=4:
	key = args[2]
	value = args[3]
	keyStore = xMind.GetXModule("keystore")
	keyStore.store(key, value)
	print("Updated ${key}:${value}")

elif (firstArg == "-gk" or firstArg == "--getkey") and args.size()>=3:
	key = args[2]
	keyStore = xMind.GetXModule("keystore")
	value = keyStore.query(key)
	if value == None:
		print("No ${key}")
	else:
		print("${key}:${value}")

elif (firstArg == "-dk" or firstArg == "--deletekey") and args.size()>=3:
	key = args[2]
	keyStore = xMind.GetXModule("keystore")
	keyStore.remove(key)
	print("Deleted ${key}")
else:
	pass

