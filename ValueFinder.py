import re
import os
import sys
import requests
import argparse
import threading
from colorama import *
from concurrent.futures import ThreadPoolExecutor

requests.packages.urllib3.disable_warnings()
init(autoreset=True)
def req(url):

	try:

		response= requests.get(url, verify=False,timeout=args.time_out, headers={"User-Agent": "Mozilla Firefox 66/55"}, allow_redirects=args.redirect)

		response.encoding = "utf-8"

		reg1 = re.findall('name=\"(.+?)\"',response.text)

		reg2 = re.findall('id=\"(.+?)\"',response.text)

		reg_document = []
		blacklist= ["?","*","<",">","#","!",";",":","<\\","</","/>"]

		r3 = re.findall("""(document\.[a-zA-Z0-9._-]+\(\".+?\"\)|document\.[a-zA-Z0-9._-]+\(\'.+?\'\))""",response.text)


		if r3:

			for i in r3:

				if '"' in i:

					i = i.split('"')

					if not i[-2] in blacklist:


						reg_document.append(i[-2])
				elif "'" in i:

					i = i.split("'")

					if not i[-2] in blacklist:


						reg_document.append(i[-2])

				else:
					pass


		reg3 = list(set(reg1 + reg2 + reg_document))

		del reg1,reg2,r3

		if len(reg3) > 0:

			if not args.combine:
				with print_lock:
					print("""

						\r{}
						\r{}
						\r{}


						""".format(Fore.YELLOW+"#"*len(url), Fore.MAGENTA+str(url), Fore.YELLOW+"#"*len(url)))

				if args.output:
					print_now(url,"çift")


			for i in reg3:

				i = i.replace("'","").replace('"','').replace(" +","").replace("+ ","").replace(" +","").replace(" ","")

				if args.combine:
					if "?" in url:
						if not i + "=" in url:
							i = url + "&" + i + "=1"
						else:
							pass
					else:
						if url.endswith("/"):
							i = url + "?" + i + "=1"
						else:
							if not url.endswith(".jpg") and not url.endswith(".png") and not url.endswith(".svg"):
								if not url.endswith(".html") and not url.endswith(".php") and not url.endswith(".asp") and not url.endswith(".aspx"):
									i = url + "/?" + i + "=1"
								else:
									i = url + "?" + i + "=1"

					with print_lock:
						print(Fore.GREEN + f"{i}")

					if args.output:
						print_now(i,"tek")
				else:
					with print_lock:
						print(Fore.GREEN + f"{i}")

					if args.output:
						print_now(i,"tek")

	except Exception as e:
		print(e)


def print_now(target,method):

	if method == "çift":

		target = """

		\r{}
		\r{}
		\r{}

		""".format("#"*len(target),target,"#"*len(target))

		with open(args.output,"a+") as file:
			file.write(str(target)+"\n\n")

	else:
		with open(args.output,"a+") as file:
			file.write(str(target)+"\n")


if __name__ == "__main__":

	ap = argparse.ArgumentParser()
	ap.add_argument("--url", metavar="", required=False, help="Target URL")
	ap.add_argument("--list", metavar="", required=False, help="Target URL List")
	ap.add_argument("--combine", required=False, action="store_true", help="Combine parameters with url.")
	ap.add_argument("--redirect", required=False, action="store_true", help="Follow Redirects")
	ap.add_argument("--output", metavar="", required=False, help="save output")
	ap.add_argument("--time-out", metavar="", required=False, default=10, type=int,help="Request Timeout(Default-10)")
	ap.add_argument("--thread", metavar="", required=False, default=10, type=int,help="Thread Number(Default-10)")

	args = ap.parse_args()

	total = []
	print_lock = threading.Lock()

	if args.list and not args.url:

		if not os.path.exists(args.list):
			print("Target List Not Found: ",args.list)
			sys.exit()

		x = open(args.list,"r", encoding="utf8").read().split("\n")
		total.extend(list(set(filter(None, x))))

		if not len(total) > 0:
			print("Your Url List Is Empty: ",args.list)
			sys.exit()

		del x

	elif args.url and not args.list:
		total.append(args.url)

	else:
		print("You Need To Use --url Or --list params")
		sys.exit()

	final = re.compile(r"http(|s)\:\/\/")
	final_ = list(filter(final.match,total))

	if not len(total) > 0:
		print("you Need To Use httpsŞ:// Or http:// Protocol For Urls")
		sys.exit()

	del final,total

	with ThreadPoolExecutor(max_workers=args.thread) as executor:
		executor.map(req, final_)
