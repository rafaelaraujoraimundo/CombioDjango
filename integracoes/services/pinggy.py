import os
import re
import shlex
import signal
import subprocess
import threading
import time
import urllib.request
import platform
import logging
import shutil

from dataclasses import dataclass
from typing import Optional
from decouple import config

IS_WINDOWS = platform.system() == "Windows"

# Host/porta do Pinggy (modelo "pro")
PINGGY_HOST = "pro.pinggy.io"
PINGGY_PORT = "443"

# Regex para capturar URL pública do stdout do pinggy via SSH
RE_HTTP_URL = re.compile(r"https?://[\w\-.]+\.pinggy\.(?:link|io)(?::\d+)?", re.IGNORECASE)
RE_TCP_URL  = re.compile(r"tcp://[\w\-.]+\.pinggy\.(?:link|io):\d+", re.IGNORECASE)

logger = logging.getLogger(__name__)

@dataclass
class TunnelResult:
    public_url: Optional[str]
    public_port: Optional[int]
    pid: Optional[int]

def _tipo_to_remote_x(tipo: str) -> str:
    """
    Mapeia tipo -> comando remoto pinggy (x:https | x:http | x:tcp)
    """
    t = (tipo or "http").lower()
    if t in ("https", "http", "tcp"):
        return f"x:{t}"
    raise ValueError("Tipo de túnel inválido. Use 'http', 'https' ou 'tcp'.")

def _build_cmd_ssh(
    tipo: str,
    token: str,
    host_local: str,
    porta_local: int,
    sni_local: Optional[str] = None,
    local_forward: Optional[str] = None
) -> list[str]:
    """
    Monta o comando com o ssh “normal” (Linux/macOS) ou plink (Windows) no formato do exemplo:
      ssh -p 443 -R0:<host_local>:<porta_local> [-L<lf>] -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -t <TOKEN>@pro.pinggy.io x:<tipo>
    - Com senha:
        * Windows: plink.exe -pw <senha>
        * Linux/macOS: sshpass -p <senha> ssh ...
    - Sem senha: ssh/plink direto
    - sni_local: se informado e tipo https, adiciona "x:https:<SNI>" (variante suportada por algumas contas).
    - local_forward: string no formato "4300:localhost:4300" (vai virar -L4300:localhost:4300)
    """
    password = config("PINGGY_PASS", default="", cast=str).strip()
    remote_x = _tipo_to_remote_x(tipo)
    if sni_local and tipo.lower() == "https":
        # algumas contas aceitam "x:https:<SNI>" como atalho; se não quiser, remova esta linha
        remote_x = f"{remote_x}:{sni_local}"

    r_arg = f"0:{host_local}:{porta_local}"
    dest = f"{token}@{PINGGY_HOST}"

    # ---------- WINDOWS: plink.exe ----------
    if IS_WINDOWS:
        plink = shutil.which("plink.exe") or shutil.which("plink")
        if not plink:
            raise RuntimeError("plink.exe (PuTTY) não encontrado no PATH. Instale o PuTTY ou adicione o plink ao PATH.")

        cmd = [
            plink, "-ssh",
            "-batch",                 # sem prompts interativos
            "-P", PINGGY_PORT,
            "-t",                     # TTY necessário p/ o Pinggy imprimir a URL
            "-R", r_arg,
        ]

        # local forward opcional: -L<spec> (ex.: -L4300:localhost:4300)
        if local_forward:
            cmd += ["-L", local_forward]

        # host key opcional (evita prompt na 1ª vez). Exemplo de valor:
        # "ssh-rsa 4096 SHA256:nFd5rfJMGuZXvfeRzJ/BtT3TfksAxTWMajcrHRcI7AM"
        hostkey = config("PINGGY_HOSTKEY", default="", cast=str).strip()
        if hostkey:
            cmd += ["-hostkey", hostkey]

        if password:
            cmd += ["-pw", password]

        # destino + comando remoto (x:https | x:http | x:tcp[, :SNI])
        cmd += [dest, remote_x]
        return cmd

    # ---------- LINUX / macOS: ssh ----------
    user_known_hosts = "/dev/null"
    ssh_opts = [
        "-p", PINGGY_PORT,
        "-o", "StrictHostKeyChecking=no",
        "-o", f"UserKnownHostsFile={user_known_hosts}",
        "-o", "ServerAliveInterval=30",
        "-o", "ExitOnForwardFailure=yes",
        "-t",                         # precisa TTY
        "-R", r_arg,
    ]

    if local_forward:
        ssh_opts += ["-L", local_forward]

    ssh_base = ["ssh", *ssh_opts, dest, remote_x]

    if password:
        sshpass = shutil.which("sshpass")
        if not sshpass:
            raise RuntimeError("Para autenticar por senha no Linux/macOS é necessário ter 'sshpass' no PATH.")
        return [sshpass, "-p", password, *ssh_base]

    return ssh_base

def start_tunnel(
    tipo: str,
    token: str,
    host_local: str,
    porta_local: int,
    sni_local: Optional[str] = None,
    local_forward: Optional[str] = None,  # ex.: "4300:localhost:4300"
    log_output_tail: int = 80,
    join_timeout: float = 20.0
) -> TunnelResult:
    """
    Inicia o túnel Pinggy e tenta extrair a URL pública da saída.
    """

    # 1) Monta o comando e registra (com senha mascarada)
    cmd = _build_cmd_ssh(tipo, token, host_local, porta_local, sni_local, local_forward)

    # mascara senha: cobre sshpass(-p <senha>) e plink(-pw <senha>)
    cmd_display_parts = []
    redact_next = False
    for i, part in enumerate(cmd):
        if redact_next:
            cmd_display_parts.append("******")
            redact_next = False
            continue
        if (i > 0 and cmd[i-1].endswith("sshpass") and part == "-p") or part == "-pw":
            cmd_display_parts.append(part)
            redact_next = True
        else:
            cmd_display_parts.append(part)
    cmd_display = shlex.join(cmd_display_parts) if hasattr(shlex, "join") else " ".join(shlex.quote(p) for p in cmd_display_parts)
    print("start_tunnel: comando montado: %s", cmd_display)

    # 2) Flags de criação (Windows) e ambiente
    creationflags = 0
    if IS_WINDOWS:
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) | 0x00000008  # DETACHED_PROCESS
        logger.debug("start_tunnel: IS_WINDOWS=True, creationflags=0x%08X", creationflags)

    env = os.environ.copy()
    logger.debug("start_tunnel: PATH parcial: %s", env.get("PATH", "")[:200])

    # 3) Lança o processo
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            creationflags=creationflags,
            env=env
        )
    except FileNotFoundError:
        logger.exception("start_tunnel: binário não encontrado ao executar o comando.")
        raise
    except Exception:
        logger.exception("start_tunnel: falha ao iniciar o processo SSH/Plink.")
        raise

    logger.info("start_tunnel: processo iniciado. PID=%s", proc.pid)

    public_url: Optional[str] = None
    public_port: Optional[int] = None
    tail: list[str] = []

    def _reader():
        nonlocal public_url, public_port
        if proc.stdout is None:
            logger.warning("start_tunnel._reader: proc.stdout é None; não será possível ler saída.")
            return

        for raw_line in proc.stdout:
            line = raw_line.rstrip("\n")
            tail.append(line)
            if len(tail) > log_output_tail:
                tail.pop(0)
            logger.debug("start_tunnel.out: %s", line)

            m = RE_HTTP_URL.search(line) or RE_TCP_URL.search(line)
            if m:
                public_url = m.group(0)
                if public_url.startswith("tcp://"):
                    try:
                        public_port = int(public_url.rsplit(":", 1)[-1])
                    except ValueError:
                        logger.warning("start_tunnel: URL TCP detectada, mas porta inválida: %r", public_url)
                        public_port = None
                logger.info("start_tunnel: URL pública detectada: %s (porta=%s)", public_url, public_port)
                break

    t = threading.Thread(target=_reader, daemon=True, name="pinggy-stdout-reader")
    t.start()
    t.join(timeout=join_timeout)

    if public_url is None:
        returncode = proc.poll()
        logger.warning(
            "start_tunnel: nenhuma URL pública detectada após %.1fs. PID=%s, returncode=%r",
            join_timeout, proc.pid, returncode
        )
        if tail:
            logger.warning("start_tunnel: últimas %d linhas da saída:\n%s",
                           len(tail), "\n".join(tail))

        if any("Permission denied" in ln for ln in tail):
            logger.error("start_tunnel: falha de autenticação (verifique TOKEN, PINGGY_PASS).")

        if IS_WINDOWS and any("host key" in ln.lower() for ln in tail):
            logger.error("start_tunnel: hostkey não cacheado. Defina PINGGY_HOSTKEY no .env ou aceite uma vez via PuTTY.")

        if returncode is not None and returncode != 0:
            logger.error("start_tunnel: processo terminou com código %s.", returncode)

    return TunnelResult(public_url=public_url, public_port=public_port, pid=proc.pid)

def stop_tunnel(pid: int) -> bool:
    try:
        if IS_WINDOWS:
            subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        else:
            os.kill(pid, signal.SIGTERM)
            time.sleep(0.5)
            return True
    except Exception:
        return False

def check_online(url: str, timeout=3) -> bool:
    try:
        if url.startswith("tcp://"):
            return True
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return 200 <= resp.status < 500
    except Exception:
        return False
