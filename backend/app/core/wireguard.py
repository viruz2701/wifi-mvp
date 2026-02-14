import subprocess
import re
from pathlib import Path

WG_INTERFACE = "wg0"
WG_CONFIG_PATH = f"/etc/wireguard/{WG_INTERFACE}.conf"

def _run_wg_cmd(*args):
    """Выполнить команду wg и вернуть вывод."""
    cmd = ["wg"] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"wg command failed: {result.stderr}")
    return result.stdout

def add_peer(public_key: str, allowed_ips: str, endpoint: str = None):
    """Добавить пир в интерфейс wg0."""
    cmd = ["wg", "set", WG_INTERFACE, "peer", public_key, "allowed-ips", allowed_ips]
    if endpoint:
        cmd += ["endpoint", endpoint]
    _run_wg_cmd(*cmd[2:])  # убираем "wg" из начала
    # Также нужно добавить пир в конфигурационный файл для сохранения при перезагрузке
    _append_peer_to_config(public_key, allowed_ips, endpoint)

def remove_peer(public_key: str):
    """Удалить пир."""
    _run_wg_cmd("set", WG_INTERFACE, "peer", public_key, "remove")
    _remove_peer_from_config(public_key)

def _append_peer_to_config(public_key: str, allowed_ips: str, endpoint: str = None):
    """Добавить секцию [Peer] в конфигурационный файл."""
    config_path = Path(WG_CONFIG_PATH)
    if not config_path.exists():
        raise FileNotFoundError(f"WireGuard config {WG_CONFIG_PATH} not found")
    with open(config_path, "a") as f:
        f.write(f"\n[Peer]\nPublicKey = {public_key}\nAllowedIPs = {allowed_ips}\n")
        if endpoint:
            f.write(f"Endpoint = {endpoint}\n")

def _remove_peer_from_config(public_key: str):
    """Удалить секцию [Peer] из конфигурационного файла."""
    config_path = Path(WG_CONFIG_PATH)
    if not config_path.exists():
        return
    with open(config_path, "r") as f:
        lines = f.readlines()
    new_lines = []
    skip = False
    for line in lines:
        if line.startswith("[Peer]") and not skip:
            skip = True
            continue
        if skip and line.startswith("PublicKey") and public_key in line:
            continue
        if skip and line.strip() == "":
            skip = False
            continue
        if not skip:
            new_lines.append(line)
    with open(config_path, "w") as f:
        f.writelines(new_lines)