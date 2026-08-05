from dataclasses import dataclass, field
import json
from datetime import datetime

from security.credential_manager import(SQL_SERVICE, NAS_SERVICE, save_password, get_password)


CONFIG_FILE = "settings.json"

@dataclass
class ConnectionConfig:
    server: str = ""
    user: str = ""
    password: str = ""
    database: str = "master"
    driver: str = "ODBC Driver 18 for SQL Server"
    selected_databases: list[str] = field(default_factory=list)
    selected_path: str = ""
    nas_user: str = ""
    nas_pass: str = ""
    auto_delete_months: int = 0
    auto_delete_days: int = 0
    schedule_enabled: bool = False
    schedule_hours: int = 0
    schedule_minutes: int = 0
    schedule_days: list[int] = field(default_factory=list)
    schedule_start: str = ""
    email_enabled: bool = False
    email_ok: list[str] = field(default_factory=list)
    email_err: list[str] = field(default_factory=list)


    
    def connection_string(self):

        return (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.user};"
            f"PWD={self.password};"
            "TrustServerCertificate=yes;"
        )

    def save(self):
        data = {
            "server": self.server,
            "user": self.user,
            "driver": self.driver,
            "database": self.database,
            "selected_databases": self.selected_databases,
            "selected_path": self.selected_path,
            "nas_user": self.nas_user,
            "auto_delete_months": self.auto_delete_months,
            "auto_delete_days": self.auto_delete_days,
            "schedule_enabled": self.schedule_enabled,
            "schedule_hours": self.schedule_hours,
            "schedule_minutes": self.schedule_minutes,
            "schedule_days": self.schedule_days,
            "schedule_start": self.schedule_start,
            "email_enabled": self.email_enabled,
            "email_ok": self.email_ok,
            "email_err": self.email_err


        }

        with open(CONFIG_FILE, "w") as file:
            json.dump(data, file, indent=4)

        
        save_password(
            SQL_SERVICE,
            self.user,
            self.password
        ) 
        if self.user:
            save_password(
                NAS_SERVICE,
                self.nas_user,
                self.nas_pass
            ) 

    @classmethod
    def load(cls):

        try:

            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            user = data.get("user", "")
            password = get_password(SQL_SERVICE, user) or ""

            nas_user = data.get("nas_user", "")
            nas_pass = ""
            if nas_user:
                nas_pass = get_password(NAS_SERVICE, nas_user) or ""


            return cls(
                server=data.get("server", ""),
                user=user,
                password=password,
                database=data.get("database", "master"),
                driver=data.get("driver", "ODBC Driver 18 for SQL Server"),
                selected_databases=data.get("selected_databases", []),
                nas_user=nas_user,
                nas_pass=nas_pass,
                selected_path=data.get("selected_path", ""),
                auto_delete_months=data.get("auto_delete_months", 0),
                auto_delete_days=data.get("auto_delete_days", 0),
                schedule_enabled=data.get("schedule_enabled", False),
                schedule_hours=data.get("schedule_hours", 0),
                schedule_minutes=data.get("schedule_minutes", 0),
                schedule_days=data.get("schedule_days", []),
                schedule_start=data.get("schedule_start", ""),
                email_enabled=data.get("email_enabled", False),
                email_ok=data.get("email_ok", []),
                email_err=data.get("email_err", [])
            )
        

        except (FileNotFoundError, json.JSONDecodeError):
            return cls()

    