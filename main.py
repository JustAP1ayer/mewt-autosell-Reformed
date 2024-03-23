#i gave up frames uses mewt too much in his code cba
try:
    import requests, os, sys, json, time, threading, copy, math
    from colorama import Fore, Style
    from rgbprint import gradient_print
except ModuleNotFoundError as error:
    os.system("pip install requests colorama rgbprint")
    os.execv(sys.executable, [sys.executable] + [sys.argv[0]] + sys.argv[1:])

settings = json.load(open("settings.json", "r"))
collectable_types = [
    8,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    41,
    64,
    65,
    68,
    67,
    66,
    69,
    72,
    70,
    71,
    72,
]

class MewtStyle():
    MAIN = f"\x1b[38;2;247;184;207m"


class Webhook:
    def __init__(self, webhook):
        self.webhook = webhook

    def post(self, buyer_name, buyer_id, item_name, item_id, price):
        payload = {
            "embeds": [
                {
                    "title": f"Sold {item_name}!",
                    "description": f"`Earned`: **{price}**\n`Buyer`: **[{buyer_name}](https://www.roblox.com/users/{buyer_id})**",
                    "url": f"https://www.roblox.com/catalog/{item_id}",
                    "color": 16234703
                }
            ]
        }
        
        with requests.session() as session:
            session.post(self.webhook, json=payload)

class Client:
    def __init__(self):
        self.version = "1"
        self.title = (f"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⢧⡀⠀⠀⢰⣶⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠁⠀⠙⢦⡀⢸⡏⠻⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠙⠺⡇⠀⠀⠙⠳⠦⡀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣠⠤⢤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡖⠶⠶⠒⠒⠒⠒⠓⠂⠀⠀⠀⠀⠀⠐⠒⠚⠛⠋⠉⠉⠉⠁⠀⠀⠀⠀⠉⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠙⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⢀⣠⣄⡀⠀⠀⠀⠀⢀⣠⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠃⠀⠀⠀⣰⠏⢉⣼⣧⠀⠀⠀⢠⣿⣅⠀⠀⢹⡆⠀⠀⠀⠀⠀⠀⢠⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡯⠀⢸⣿⣿⠀⠀⠀⣾⣿⣿⠀⠀⠀⣷⠀⠀⠀⠀⠀⢀⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⠁⢀⠈⠁⠀⢸⣿⣿⠀⠀⠀⢹⣿⣿⠀⠀⠀⠉⠀⠀⠀⠈⠛⢿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡀⠀⠀⢸⣧⣴⣀⣄⠉⣁⠐⣳⢀⣨⣟⠋⠀⠀⣀⣴⣠⠀⠀⠀⢀⡼⠃⠀⠀⠀⢰⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢶⡎⢳⣌⡉⠀⠀⠙⠻⣯⣉⢉⣿⠄⠀⠀⢉⣬⡿⠃⠀⠀⢾⡀⠀⠀⠀⠀⣸⠃⠙⠳⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣇⣀⡈⠙⠛⢳⡶⣤⣤⣭⣽⣭⡴⣶⠛⣿⣥⡄⢠⣤⣤⣼⡇⠀⡄⣾⠀⣿⠀⠀⠀⠀⠙⢦⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢰⡟⠛⠺⠷⢤⣤⣿⣿⣿⣤⡾⠟⣃⡿⠀⠀⠀⠀⠀⠀⠘⠃⡿⢀⡗⠀⠀⠀⠀⠀⠈⢻⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣆⠀⠀⠀⢸⣏⣌⡙⡇⠀⠀⠺⣦⠀⠀⠀⠀⠀⠀⣼⣄⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠹⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢙⣷⠀⠀⠀⠛⠛⠛⠁⠀⠀⣾⠁⠀⠀⠀⠀⠀⢰⡟⢹⣆⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡏⠁⠀⠀⠀⠀⣤⠀⠀⠀⢰⣾⠀⠀⠀⠀⠀⣠⡟⠀⠀⠿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⡟⠛⠛⠀⣠⡟⠀⠀⠀⢸⢹⡄⠀⠀⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡇⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⣿⡇⠀⠀⠀⢸⠸⣇⣀⡴⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⢻⠀⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠀⠀⠀⣿⠀⠀⠀⠀⣿⠀⠻⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⢼⣰⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡶⠶⠛⠋⣿⠀⠀⢠⡏⠀⠀⠀⠀⡿⠀⠀⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⢁⡿⠾⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⠿⠀⠀⠀⣿⠀⠀⣸⠃⠀⠀⠀⢠⡏⠀⠀⠀⠀⢹⡷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠈⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⣟⠁⠀⠀⠀⠀⢶⣿⠀⢠⡟⠀⠀⠀⠀⢸⠅⠀⠀⠀⠀⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠃⠀⠀⠀⠀⠘⣿⢀⡾⠁⠀⠀⠀⠀⣿⠀⠀⠀⠀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠿⢦⣄⡀⠀⠀⠀⠀⡏⣼⠃⠀⠀⠀⠀⢀⡿⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⢠⣄⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣴⠟⠓⠤⡀⠈⠹⣦⡀⠀⠐⣷⣷⡇⠀⢠⡄⠀⣼⣃⣀⣀⣀⠀⠀⡇⠀⠀⠀⠲⣄⡀⠀⠀⠀⣈⡽⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⠿⠅⣀⠀⠀⠈⠳⡄⠸⣧⠀⣠⡿⠿⢷⢤⣬⣿⡾⠛⠉⠉⠉⠉⠷⣴⡇⠀⠀⠀⠀⠈⠙⠛⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣠⡾⢁⡀⠀⠀⠑⢄⠀⠀⠸⣄⣿⠟⠉⠀⠀⠀⠀⠀⢸⣇⠤⠤⠦⠤⠤⢀⣹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣴⠋⠀⠀⠈⠑⢄⠀⠀⢣⠀⣠⡟⠁⠀⠀⠀⠀⠀⠀⠀⢸⠇⠀⠀⠀⠀⠀⠀⠉⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢰⡏⣴⠉⠑⣢⣄⠀⠀⢳⣀⣴⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⠿⣏⠀⠀⢿⠀⣳⣤⡶⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣀⣀⡀⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠋⠙⠛⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠉⠓⠢⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣀⠀⣀⣀⡀⠀⣸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⢰⡇⠀⠀⢿⢑⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣷⣀⣤⣼⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        :3""")

        self.ready = False    
        self.blacklist = settings["BLACKLIST"]
        self.webhook_enabled = settings["WEBHOOK"]["ENABLED"]
        self.webhook_url = settings["WEBHOOK"]["URL"]
        self.client = {
            "cookie": settings["COOKIE"],
            "auth": "abcabcabc",
            "name": "abcabcabc",
            "id": 0
        }
        self.inventory = {}
        self.last_transaction_id = None
        self.raw_inventory = []
        self.onsale = []
        

        self.id_to_name = {}
        self.collectable_id_to_name = {}

        self.collectable_instance_id_to_product_id = {}

        self.collectable_id_to_id = {}

        self.webhook = None

        self.session = requests.session()
        self.session.cookies['.ROBLOSECURITY'] = self.client["cookie"]

        self.resellable_count = 0
        self.logs = []

        if self.webhook_enabled:
            self.webhook = Webhook(self.webhook_url)



        self.verify_cookie()
        while self.ready != True:
            time.sleep(1)

        
        self.infinite_thread(self.update_status, 1)
        self.infinite_thread(self.set_token, 200)

        self.logs.append(f"Logged in as {self.client['name']}({self.client['id']})")
        self.logs.append("Fetching inventory this may take a minute, please wait.")
        self.infinite_thread(self.fetch_inventory)
        self.infinite_thread(self.sell_all_items, 5)
        self.infinite_thread(self.scan_recent_transactions, 3 * 60)

    def update_status(self):
        os.system('cls' if os.name=='nt' else 'clear')
        gradient_print(self.title, start_color=(0xFF6EA3), end_color=(0xF7B8CF))
        print(Fore.RESET + Style.RESET_ALL)
        print(Style.BRIGHT + f"> Current User: {MewtStyle.MAIN}{Style.BRIGHT}{self.client['name']}{Fore.WHITE}{Style.BRIGHT} ")
        print(Style.BRIGHT + f"> Resellable Items: {MewtStyle.MAIN}{Style.BRIGHT}{self.resellable_count}{Fore.WHITE}{Style.BRIGHT} ")
        print()
        print(Style.BRIGHT + f"> Logs: {MewtStyle.MAIN}{Style.BRIGHT}\n" + "\n".join(log for log in self.logs[-10:]) + f"{Fore.WHITE}{Style.BRIGHT}")

    

    def verify_cookie(self):
        conn = self.session.get("https://users.roblox.com/v1/users/authenticated")
        if(conn.status_code == 200):
            data = conn.json()
            self.client["id"] = data["id"]
            self.client["name"] = data["name"]
            self.ready = True
        else:
            print("Invalid cookie or please wait a minute and trying again")
            time.sleep(1)
            raise SystemExit
        
    def set_token(self):
        try:
            conn = self.session.post("https://friends.roblox.com/v1/users/1/request-friendship")
            if(conn.headers.get("x-csrf-token")):
                self.client["auth"] = conn.headers["x-csrf-token"]
                self.session.headers["x-csrf-token"] = conn.headers["x-csrf-token"]
        except:
            time.sleep(5)
            return self.set_token()

    def scan_recent_transactions(self):
        try:
            conn = self.session.get(f"https://economy.roblox.com/v2/users/{self.client['id']}/transactions?cursor=&limit=100&transactionType=Sale")
            if(conn.status_code == 200):
                conn_data = conn.json()
                data = conn_data["data"]
                if self.last_transaction_id is None:
                    self.last_transaction_id = data[0]["idHash"]
                    return 
                
                for sale in data:
                    if sale["idHash"] == self.last_transaction_id:
                        self.last_transaction_id = data[0]["idHash"] 
                        break 
                    
                    agentId = sale['agent']['id']
                    agentName = sale['agent']['name']
                    assetId = sale['details']['id']
                    assetName = sale['details']['name']
                    assetType = sale['details']['type']
                    amount = sale['currency']['amount']
                    if assetType != 'Asset':
                        continue

                    

                    self.logs.append(f"{agentName} bought {assetName}, you earned {amount}!")
                    if self.webhook_enabled:
                        self.webhook.post(agentName, agentId, assetName, assetId,  amount)
            else:
                time.sleep(15)
                return self.scan_recent_transactions()

        except Exception as error:
            print(error)
            time.sleep(15)
            return self.scan_recent_transactions()

    def fetch_inventory(self, assettype, cursor = "", data = []):
        try:
            conn = self.session.get(f"https://inventory.roblox.com/v2/users/{self.client['id']}/inventory/{assettype}?cursor={cursor}&limit=100&sortOrder=Desc")
            if(conn.status_code == 200):
                conn_data = conn.json()
                data = data + conn_data["data"]

                if conn_data["nextPageCursor"] is not None:
                    return self.fetch_inventory(assettype, conn_data["nextPageCursor"], data)
                
                return data
            elif(conn.status_code == 429):
                time.sleep(5)
                return self.fetch_inventory(assettype, cursor, data)
        except:
            time.sleep(5)
            return self.fetch_inventory(assettype, cursor, data)

        
    def fetch_item_resellable(self, collectableItemId, cursor = "", data = []):
        try:
            conn = self.session.get(f"https://apis.roblox.com/marketplace-sales/v1/item/{collectableItemId}/resellable-instances?cursor={cursor}&ownerType=User&ownerId={self.client['id']}&limit=500")
            if(conn.status_code == 200):
                conn_data = conn.json()
                data = data + conn_data["itemInstances"]
                if conn_data["nextPageCursor"] is not None:
                    return self.fetch_item_resellable(collectableItemId, conn_data["nextPageCursor"], data)
                
                return data
            else:
                time.sleep(10)
                return self.fetch_item_resellable(collectableItemId, cursor, data)
        except:
            time.sleep(5)
            return self.fetch_item_resellable(collectableItemId, cursor, data)
        
    def fetch_item_details(self, items):
        try:
            conn = self.session.post("https://apis.roblox.com/marketplace-items/v1/items/details", json={ "itemIds": items })
            if(conn.status_code == 200):
                conn_data = conn.json()
                return conn_data
            else:
                time.sleep(5)
                return self.fetch_item_details(items)
        except:
            time.sleep(5)
            return self.fetch_item_details(items)
        
    def fetch_reseller(self, collectableItemId):
        try:
            conn = self.session.get(f"https://apis.roblox.com/marketplace-sales/v1/item/{collectableItemId}/resellers?limit=1")
            if(conn.status_code == 200):
                 conn_data = conn.json()
                 return conn_data["data"][0]
            else:
                time.sleep(5)
                return self.fetch_reseller(collectableItemId)
        except:
            time.sleep(5)
            return self.fetch_reseller(collectableItemId)

    
    def sell_item(self, price, collectibleItemId, collectibleInstanceId, collectibleProductId):
        try:
            number = price * 0.5  # Fees
            while not number >= math.ceil(number):
                price = price - 1
                number = price * 0.5
            payload = {
                "collectibleProductId": collectibleProductId,
                "isOnSale": True,
                "price": price,
                "sellerId": self.client["id"],
                "sellerType": "User",
            }
            conn = self.session.patch(f"https://apis.roblox.com/marketplace-sales/v1/item/{collectibleItemId}/instance/{collectibleInstanceId}/resale", json=payload)
            if(conn.status_code == 200):
                return True
            else:
                time.sleep(10)
                return self.sell_item(price, collectibleItemId, collectibleInstanceId, collectibleProductId)
        except:
            time.sleep(10)
            return self.sell_item(price, collectibleItemId, collectibleInstanceId, collectibleProductId)
        
    def sell_all_items(self):   
        try:
           for item_id, item_info in self.inventory.items():
                if not item_id in self.blacklist:
                    for instance_id, instance_info in item_info.items():
                        if instance_info['resellable']:
                            resell_info = self.fetch_reseller(item_id)
                            if resell_info:
                                resell_price = resell_info['price']
                                self.sell_item(resell_price, item_id, instance_id, instance_info['collectableProductId'])
                            else:
                                print(f"Could not fetch resell info for item {item_id}. Skipping...")
                        else:
                            print(f"Item {item_id} is not resellable. Skipping...")
        except Exception as error:
            print(f"Error in sell_all_items: {error}")

    def infinite_thread(self, func, _time):
        def _func():
            while True:
                func()
                time.sleep(_time)
        threading.Thread(target=_func,).start()

if __name__ == '__main__':
    Client()
