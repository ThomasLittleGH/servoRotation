#!/usr/bin/env python3
import time
import board
import busio
from adafruit_pca9685 import PCA9685

# -------------------------------
# Inicialización del PCA9685
# -------------------------------
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # 50 Hz → período de 20,000 μs

# Usamos el canal 4 para el servo
SERVO_CHANNEL = pca.channels[4]

# -------------------------------
# Valores de pulso (en μs)
# -------------------------------
STOP_PULSE    = 1500  # Pulso neutro (servo parado)
FORWARD_PULSE = 1588  # Pulso para rotación en sentido positivo
REVERSE_PULSE = 1470  # Pulso para rotación en sentido negativo

# -------------------------------
# Datos de rotación basados en mediciones
# -------------------------------
# Para sentido positivo: 360° en 4.83 s → tasa ≈ 74.5°/s
rotation_rate_positive = 360.0 / 5.5

# Para sentido negativo: 360° en 4.68 s → tasa ≈ 76.9°/s
rotation_rate_negative = 360.0 / 5.5

def set_servo_pulse(channel, pulse_us):
    """
    Convierte el ancho de pulso (en μs) a un duty cycle de 16 bits y lo aplica al canal.
    """
    duty_cycle = int((pulse_us / 20000) * 0xFFFF)
    channel.duty_cycle = duty_cycle

def rotate_degrees(degrees):
    """
    Rota el servo de rotación continua la cantidad de grados especificada.
    Usa FORWARD_PULSE para grados positivos y REVERSE_PULSE para grados negativos.
    Calcula el tiempo de rotación en base a la tasa de giro medida.
    """
    if degrees > 0:
        pulse = FORWARD_PULSE
        rate = rotation_rate_positive
    elif degrees < 0:
        pulse = REVERSE_PULSE
        rate = rotation_rate_negative
    else:
        print("No se rota (0°).")
        return

    duration = abs(degrees) / rate
    print(f"Rotando {degrees:.1f}° durante {duration:.2f} segundos (pulso = {pulse} μs)")
    set_servo_pulse(SERVO_CHANNEL, pulse)
    time.sleep(duration)
    set_servo_pulse(SERVO_CHANNEL, STOP_PULSE)
    print("Rotación completada. Servo detenido.")

def main():
    try:
        while True:
            user_input = input("Ingresa los grados a rotar (positivo/negativo) o 'q' para salir: ").strip()
            if user_input.lower() == 'q':
                break
            try:
                deg = float(user_input)
                rotate_degrees(deg)
            except ValueError:
                print("Error: Ingresa un número válido.")
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
    finally:
        set_servo_pulse(SERVO_CHANNEL, STOP_PULSE)
        pca.deinit()
        print("PCA9685 apagado. Saliendo.")

if __name__ == "__main__":
    main()
