import json
import os

BOT_CONFIG_PATH = "datas/bot.json"

default_config = {
  "discord_token": "",
  "mcplayhd_token": "",
  "folders": {
    "cogs": "cogs/",
    "logs": "logs/",
    "datas": "datas/",
    "guilds": "guilds/"
  },
  "debug": {
      "guilds": []
  },
  "google_sheet": {
      "id": ""
  }
}


class _References:
    def __init__(self):
        self.load()
        self.config = {}

    def load(self):
        if not os.path.exists(BOT_CONFIG_PATH):
            print(f"The config file '{BOT_CONFIG_PATH}' don't exist, a new one will be created")
            self.create_config()
        else:
            with open(BOT_CONFIG_PATH, "r") as cfg:
                self.config = json.load(cfg)

        self.DISCORD_TOKEN = self.config["discord_token"]
        self.MCPLAYHD_TOKEN = self.config["mcplayhd_token"]

        self.FOLDER_COGS = self.config["folders"]["cogs"]
        self.FOLDER_LOGS = self.config["folders"]["logs"]
        self.FOLDER_DATAS = self.config["folders"]["datas"]
        self.FOLDER_GUILDS = self.config["folders"]["guilds"]

        self.DEBUG_GUILDS = self.config["debug"]["guilds"]

        self.SHEET_ID = self.config["google_sheet"]["id"]

    def create_config(self):
        self.config = self.fill_config(dict(default_config)) # duplicate and fill the default config
        with open(BOT_CONFIG_PATH, "w") as cfg:
            json.dump(self.config, cfg, indent=4)

    def fill_config(self, config: dict):
        items = list(config.items())

        for key, value in items:
            if isinstance(value, dict):
                config[key] = self.fill_config(value)
            elif isinstance(value, str):
                if value == "":
                    while (new_value := input(f"{key} > ")) == "":
                        print("You must add a value")
                    config[key] = new_value
                elif new_value := input(f"{key} ({value}) > ") != "":
                    config[key] = new_value
        return config

    def guilds_folder(self) -> str:
        return os.path.join(self.FOLDER_DATAS, self.FOLDER_GUILDS)

    def guild_folder(self, guild_id: int, *end) -> str:
        return os.path.join(self.guilds_folder(), str(guild_id), *end)

References = _References()
