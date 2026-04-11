"""
Scheduler - Ejecución automática de estrategias

Configura jobs que corren durante horario de mercado.
"""

import schedule
import time
from datetime import datetime
from typing import Callable, Optional


class TradingScheduler:
    """Programador de tareas de trading"""

    def __init__(self):
        self.jobs = []
        self.is_running = False

    def schedule_every(
        self,
        interval: str,
        func: Callable,
        days: Optional[list] = None,
        at_time: Optional[str] = None,
    ):
        """
        Programa una función para ejecutarse periódicamente

        Args:
            interval: 'seconds', 'minutes', 'hours', 'days', 'weeks'
            func: Función a ejecutar
            days: Días de la semana (ej: ['monday', 'tuesday'])
            at_time: Hora específica (ej: '09:30')
        """
        job = None

        if at_time:
            # Ejecución a hora específica
            if days:
                for day in days:
                    job = getattr(schedule.every(), day).at(at_time).do(func)
            else:
                job = schedule.every().day.at(at_time).do(func)
        else:
            # Ejecución periódica
            if interval == "seconds":
                job = schedule.every(5).seconds.do(func)
            elif interval == "minutes":
                job = schedule.every(5).minutes.do(func)
            elif interval == "hours":
                job = schedule.every().hour.do(func)

        if job:
            self.jobs.append(job)
            print(f"✅ Job programado: {func.__name__}")

    def schedule_market_hours(
        self,
        func: Callable,
        interval_minutes: int = 5,
        market_start: str = "09:30",
        market_end: str = "16:00",
    ):
        """
        Programa una función para ejecutarse cada X minutos durante horario de mercado

        Args:
            func: Función a ejecutar
            interval_minutes: Intervalo en minutos
            market_start: Apertura del mercado (EST)
            market_end: Cierre del mercado (EST)
        """
        # Programar para cada hora durante mercado
        start_hour, start_min = map(int, market_start.split(":"))
        end_hour, end_min = map(int, market_end.split(":"))

        for day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
            current_hour = start_hour
            current_min = start_min

            while (current_hour < end_hour) or (current_hour == end_hour and current_min < end_min):
                time_str = f"{current_hour:02d}:{current_min:02d}"
                getattr(schedule.every(), day).at(time_str).do(func)

                current_min += interval_minutes
                if current_min >= 60:
                    current_min = 0
                    current_hour += 1

        print(f"✅ Market hours scheduler: {func.__name__} cada {interval_minutes} min")

    def run_pending(self):
        """Ejecuta jobs pendientes"""
        schedule.run_pending()

    def run_loop(self):
        """Loop principal del scheduler"""
        self.is_running = True
        print("🕐 Scheduler iniciado...")

        while self.is_running:
            self.run_pending()
            time.sleep(1)

    def stop(self):
        """Detiene el scheduler"""
        self.is_running = False
        schedule.clear()
        print("🛑 Scheduler detenido")


# ========== Ejemplo de uso ==========

if __name__ == "__main__":
    scheduler = TradingScheduler()

    def check_trailing_stop():
        print("📊 Verificando trailing stop...")
        # Lógica de trailing stop aquí

    def check_wheel_strategy():
        print("🎡 Verificando wheel strategy...")
        # Lógica de wheel strategy aquí

    # Programar durante horario de mercado
    scheduler.schedule_market_hours(check_trailing_stop, interval_minutes=5)
    scheduler.schedule_market_hours(check_wheel_strategy, interval_minutes=15)

    # Iniciar loop
    try:
        scheduler.run_loop()
    except KeyboardInterrupt:
        scheduler.stop()
