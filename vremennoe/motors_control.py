import time
import RPi.GPIO as GPIO

class MotorController:
    def __init__(self, en_pin, in1_pin, in2_pin):
        """
        Инициализация двигателя.
        :param en_pin: Пин для ШИМ (управление скоростью)
        :param in1_pin: Пин направления 1
        :param in2_pin: Пин направления 2
        """
        self.en_pin = en_pin
        self.in1_pin = in1_pin
        self.in2_pin = in2_pin

        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.en_pin, GPIO.OUT)
        GPIO.setup(self.in1_pin, GPIO.OUT)
        GPIO.setup(self.in2_pin, GPIO.OUT)

        # Инициализация ШИМ
        self.pwm = GPIO.PWM(self.en_pin, 1000)  # Частота 1 кГц
        self.pwm.start(0)  # Запуск с 0% скорости

    def set_speed(self, speed):
        """
        Установка скорости двигателя (0-100%).
        """
        if speed < 0 or speed > 100:
            raise ValueError("Скорость должна быть в диапазоне 0-100")
        self.pwm.ChangeDutyCycle(speed)

    def forward(self):
        """Движение вперед"""
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)

    def backward(self):
        """Движение назад"""
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)

    def stop(self):
        """Остановка двигателя"""
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        self.set_speed(0)

    def cleanup(self):
        """Очистка ресурсов GPIO"""
        self.stop()
        self.pwm.stop()
        GPIO.cleanup()

# добавляем функцию плавного изменения скорости

class SmoothSpeed:
    def init(self, initial_speed=0, smoothing=0.1):
        self.current_speed = initial_speed
        self.target_speed = initial_speed
        self.smoothing = smoothing  # Коэффициент сглаживания (0 < smoothing < 1)

    def set_target(self, target):
        self.target_speed = target

    def update(self):
        # Плавное изменение скорости
        self.current_speed += (self.target_speed - self.current_speed) * self.smoothing
        return self.current_speed

# Пример использования
if __name__ == "__main__":
    try:
        # Настройка пинов (замените на свои значения)
        motor_left = MotorController(en_pin=18, in1_pin=23, in2_pin=24)
        motor_right = MotorController(en_pin=19, in1_pin=25, in2_pin=26)

        # Движение вперед
        print("Движение вперед")
        motor_left.forward()
        motor_right.forward()
        motor_left.set_speed(50)  # 50% скорости
        motor_right.set_speed(50)
        time.sleep(2)

        # Поворот
        print("Поворот направо")
        motor_left.set_speed(75)
        motor_right.set_speed(25)
        time.sleep(1)

        # Остановка
        print("Остановка")
        motor_left.stop()
        motor_right.stop()
        time.sleep(1)

    except KeyboardInterrupt:
        print("Прервано пользователем")
    finally:
        motor_left.cleanup()
        motor_right.cleanup()
