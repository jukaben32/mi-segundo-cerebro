"""
═══════════════════════════════════════════════════════════════════════════
NOTIFICATION SYSTEM - WEBHOOKS & ALERTAS
═══════════════════════════════════════════════════════════════════════════
Sistema de notificaciones multi-canal para alertas de trading.

Canales soportados:
- Discord Webhook
- Slack Webhook
- Telegram Bot
- Email (SMTP)
- Push notifications (Pushover)
- SMS (Twilio)

Tipos de alertas:
- Trade ejecutado
- Stop loss activado
- Take profit alcanzado
- Risk breach (drawdown, VaR)
- Market events (VIX spike, etc.)
"""

import json
import smtplib
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import hmac


@dataclass
class TradeAlert:
    """Alerta de trade ejecutado"""
    symbol: str
    side: str
    quantity: float
    price: float
    pnl: Optional[float] = None
    reason: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class RiskAlert:
    """Alerta de riesgo"""
    alert_type: str  # drawdown, var, concentration
    current_value: float
    threshold: float
    message: str
    severity: str = "warning"  # warning, critical
    timestamp: datetime = field(default_factory=datetime.now)


class NotificationChannel:
    """Clase base para canales de notificación"""

    def send(self, title: str, message: str, color: str = "info") -> bool:
        raise NotImplementedError


class DiscordWebhook(NotificationChannel):
    """Envía notificaciones a Discord via webhook"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, title: str, message: str, color: str = "info") -> bool:
        """Envía embed a Discord"""
        color_map = {
            "info": 0x58a6ff,      # Blue
            "success": 0x3fb950,   # Green
            "warning": 0xd29922,   # Yellow
            "critical": 0xf85149,  # Red
        }

        embed = {
            "title": title,
            "description": message,
            "color": color_map.get(color, 0x58a6ff),
            "timestamp": datetime.now().isoformat(),
            "footer": {
                "text": "Alpaca Trading Bot",
            },
        }

        try:
            response = requests.post(
                self.webhook_url,
                json={"embeds": [embed]},
                timeout=10,
            )
            return response.status_code == 204
        except Exception as e:
            print(f"❌ Error enviando a Discord: {e}")
            return False


class SlackWebhook(NotificationChannel):
    """Envía notificaciones a Slack via webhook"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, title: str, message: str, color: str = "info") -> bool:
        """Envía message block a Slack"""
        color_map = {
            "info": "#58a6ff",
            "success": "#3fb950",
            "warning": "#d29922",
            "critical": "#f85149",
        }

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{title}*\n{message}",
                },
            },
        ]

        try:
            response = requests.post(
                self.webhook_url,
                json={
                    "blocks": blocks,
                    "attachments": [{
                        "color": color_map.get(color, "#58a6ff"),
                    }],
                },
                timeout=10,
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error enviando a Slack: {e}")
            return False


class TelegramBot(NotificationChannel):
    """Envía notificaciones via Telegram Bot"""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send(self, title: str, message: str, color: str = "info") -> bool:
        """Envía mensaje a Telegram"""
        emoji_map = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "critical": "🚨",
        }

        text = f"{emoji_map.get(color, 'ℹ️')} *{title}*\n\n{message}"

        try:
            response = requests.post(
                self.api_url,
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "Markdown",
                },
                timeout=10,
            )
            return response.json().get("ok", False)
        except Exception as e:
            print(f"❌ Error enviando a Telegram: {e}")
            return False


class EmailNotifier(NotificationChannel):
    """Envía notificaciones via Email (SMTP)"""

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        from_email: str,
        to_emails: List[str],
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.to_emails = to_emails

    def send(self, title: str, message: str, color: str = "info") -> bool:
        """Envía email"""
        msg = MIMEMultipart()
        msg["From"] = self.from_email
        msg["To"] = ", ".join(self.to_emails)
        msg["Subject"] = f"[Alpaca Trading] {title}"

        # HTML body
        color_map = {
            "info": "#58a6ff",
            "success": "#3fb950",
            "warning": "#d29922",
            "critical": "#f85149",
        }

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #0d1117; color: #f0f6fc; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: #161b22; border-radius: 8px; padding: 20px; border-left: 4px solid {color_map.get(color, '#58a6ff')};">
                <h2 style="color: {color_map.get(color, '#58a6ff')};">{title}</h2>
                <p style="line-height: 1.6;">{message}</p>
                <hr style="border: none; border-top: 1px solid #30363d; margin: 20px 0;">
                <p style="color: #8b949e; font-size: 12px;">Alpaca Trading Bot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"❌ Error enviando email: {e}")
            return False


class PushoverNotifier(NotificationChannel):
    """Envía notificaciones push via Pushover"""

    def __init__(self, api_token: str, user_key: str):
        self.api_token = api_token
        self.user_key = user_key
        self.api_url = "https://api.pushover.net/1/messages.json"

    def send(self, title: str, message: str, color: str = "info") -> bool:
        """Envía push notification"""
        priority_map = {
            "info": 0,
            "success": 0,
            "warning": 1,
            "critical": 2,  # Requiere confirmación
        }

        try:
            response = requests.post(
                self.api_url,
                json={
                    "token": self.api_token,
                    "user": self.user_key,
                    "title": title,
                    "message": message,
                    "priority": priority_map.get(color, 0),
                },
                timeout=10,
            )
            return response.json().get("status", 0) == 1
        except Exception as e:
            print(f"❌ Error enviando a Pushover: {e}")
            return False


# ═══════════════════════════════════════════════════════════════════════
# NOTIFICATION MANAGER
# ═══════════════════════════════════════════════════════════════════════

class NotificationManager:
    """
    Gestor central de notificaciones.

    Configura múltiples canales y envía notificaciones
    basadas en el tipo y severidad del evento.
    """

    def __init__(self):
        self.channels: Dict[str, NotificationChannel] = {}
        self.alert_history: List[Dict[str, Any]] = []
        self.rate_limits: Dict[str, datetime] = {}

    def add_channel(self, name: str, channel: NotificationChannel):
        """Agrega un canal de notificación"""
        self.channels[name] = channel
        print(f"✅ Canal agregado: {name}")

    def send_trade_alert(self, alert: TradeAlert):
        """Envía alerta de trade ejecutado"""
        if self._check_rate_limit(f"trade_{alert.symbol}", limit_seconds=5):
            return

        title = f"{'🟢' if alert.side == 'BUY' else '🔴'} {alert.side} {alert.symbol}"

        message = f"""
• Cantidad: {alert.quantity}
• Precio: ${alert.price:.2f}
• {'Razón: ' + alert.reason if alert.reason else ''}
        """.strip()

        color = "success" if alert.side == "BUY" else "info"
        self._broadcast(title, message, color)

        self._log_alert("trade", alert)

    def send_risk_alert(self, alert: RiskAlert):
        """Envía alerta de riesgo"""
        if self._check_rate_limit(f"risk_{alert.alert_type}", limit_seconds=60):
            return

        emoji = "🚨" if alert.severity == "critical" else "⚠️"
        title = f"{emoji} RISK ALERT: {alert.alert_type.upper()}"

        message = f"""
• Valor actual: {alert.current_value:.2f}
• Threshold: {alert.threshold:.2f}
• {alert.message}
        """.strip()

        self._broadcast(title, message, alert.severity)

        self._log_alert("risk", alert)

    def send_position_update(self, symbol: str, unrealized_pnl: float, pnl_percent: float):
        """Envía actualización de posición"""
        if abs(pnl_percent) < 5:  # Solo si P&L > 5%
            return

        if self._check_rate_limit(f"position_{symbol}", limit_seconds=300):
            return

        emoji = "📈" if unrealized_pnl >= 0 else "📉"
        title = f"{emoji} {symbol} Position Update"

        message = f"""
• P&L: ${unrealized_pnl:.2f}
• P&L %: {pnl_percent:.2f}%
        """.strip()

        color = "success" if unrealized_pnl >= 0 else "warning"
        self._broadcast(title, message, color)

    def _broadcast(self, title: str, message: str, color: str = "info"):
        """Envía notificación a todos los canales"""
        for name, channel in self.channels.items():
            try:
                channel.send(title, message, color)
            except Exception as e:
                print(f"❌ Error en canal {name}: {e}")

    def _check_rate_limit(self, key: str, limit_seconds: int) -> bool:
        """Verifica rate limiting para evitar spam"""
        now = datetime.now()
        last_sent = self.rate_limits.get(key)

        if last_sent and (now - last_sent).total_seconds() < limit_seconds:
            return True  # Rate limited

        self.rate_limits[key] = now
        return False

    def _log_alert(self, alert_type: str, alert: Any):
        """Registra alerta en histórico"""
        self.alert_history.append({
            "type": alert_type,
            "data": alert.__dict__,
            "timestamp": datetime.now(),
        })

        # Mantener solo últimos 100 alerts
        if len(self.alert_history) > 100:
            self.alert_history = self.alert_history[-100:]

    def get_alert_history(self) -> List[Dict[str, Any]]:
        """Retorna histórico de alertas"""
        return self.alert_history


# ═══════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN Y EJEMPLO DE USO
# ═══════════════════════════════════════════════════════════════════════

def setup_notification_manager(config: Dict[str, Any]) -> NotificationManager:
    """Configura el Notification Manager desde un diccionario"""
    manager = NotificationManager()

    # Discord
    if config.get("discord_webhook"):
        manager.add_channel(
            "discord",
            DiscordWebhook(config["discord_webhook"]),
        )

    # Slack
    if config.get("slack_webhook"):
        manager.add_channel(
            "slack",
            SlackWebhook(config["slack_webhook"]),
        )

    # Telegram
    if config.get("telegram_token") and config.get("telegram_chat_id"):
        manager.add_channel(
            "telegram",
            TelegramBot(config["telegram_token"], config["telegram_chat_id"]),
        )

    # Email
    if config.get("smtp_server"):
        manager.add_channel(
            "email",
            EmailNotifier(
                smtp_server=config["smtp_server"],
                smtp_port=config.get("smtp_port", 587),
                username=config["smtp_username"],
                password=config["smtp_password"],
                from_email=config["smtp_from"],
                to_emails=config["email_recipients"],
            ),
        )

    # Pushover
    if config.get("pushover_token") and config.get("pushover_user"):
        manager.add_channel(
            "pushover",
            PushoverNotifier(config["pushover_token"], config["pushover_user"]),
        )

    return manager


# Ejemplo de configuración
EXAMPLE_CONFIG = {
    # Discord: Generar webhook en Server Settings > Integrations
    "discord_webhook": "https://discord.com/api/webhooks/...",

    # Slack: Generar webhook en App Settings > Incoming Webhooks
    "slack_webhook": "https://hooks.slack.com/services/...",

    # Telegram: Crear bot con @BotFather y obtener chat_id
    "telegram_token": "YOUR_BOT_TOKEN",
    "telegram_chat_id": "YOUR_CHAT_ID",

    # Email SMTP (ejemplo: Gmail)
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_username": "tu_email@gmail.com",
    "smtp_password": "tu_app_password",
    "smtp_from": "tu_email@gmail.com",
    "email_recipients": ["tu_email@gmail.com"],

    # Pushover: Registrar app en pushover.net
    "pushover_token": "YOUR_API_TOKEN",
    "pushover_user": "YOUR_USER_KEY",
}


if __name__ == "__main__":
    print("=" * 70)
    print("NOTIFICATION SYSTEM - Demo")
    print("=" * 70)

    # Setup (sin credenciales reales para demo)
    manager = NotificationManager()

    # Simular alertas
    print("\n📪 Simulando alertas...\n")

    # Trade alert
    trade_alert = TradeAlert(
        symbol="TSLA",
        side="BUY",
        quantity=10,
        price=250.00,
        reason="Trailing Stop Strategy - Initial Entry",
    )
    manager.send_trade_alert(trade_alert)

    # Risk alert
    risk_alert = RiskAlert(
        alert_type="drawdown",
        current_value=0.08,
        threshold=0.05,
        message="Drawdown diario excede threshold del 5%",
        severity="warning",
    )
    manager.send_risk_alert(risk_alert)

    # Position update
    manager.send_position_update("TSLA", 1250.00, 5.0)

    print(f"\n📋 Histórico de alertas: {len(manager.alert_history)}")
    for alert in manager.alert_history[-3:]:
        print(f"  - {alert['type']}: {alert['data']}")

    print("\n💡 Para habilitar notificaciones reales, configura EXAMPLE_CONFIG")
