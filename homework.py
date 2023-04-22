from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Датакласс сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    # Константа шаблона сообщения.
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вывод сообщения о тренировке."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Длина шага при беге или ходьбе.
    M_IN_KM: int = 1000  # Коэффициент перевода значений из метров в километры.
    COEF_MIN: int = 60  # Коэффициент перевода значений из часов в минуты.

    """Конструктор базового класса."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Дочерний класс должен реализовать метод')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = type(self).__name__
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        duration = self.duration
        return InfoMessage(training_type, duration,
                           distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIP: int = 18  # Коэффициент № 1
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79  # Коэффициент № 2

    def get_spent_calories(self) -> float:
        """Собственный метод дочернего класса для подсчета калории."""
        return ((self.CALORIES_MEAN_SPEED_MULTIP * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * (self.duration * self.COEF_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    RATIO_WALK_1: float = 0.035
    # Коэффициент для подсчета калорий при ходьбе № 1.
    RATIO_WALK_2: float = 0.029
    # Коэффициент для подсчета калорий при ходьбе № 2.
    COEF_SPEED: float = 0.278
    # Коэффициент превода из км/ч в м/с.
    COEF_HEIGHT: int = 100
    # Коэффициент превода см в м.

    """Конструктор дочернего класса - ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Собственный метод дочернего класса для подсчета калории."""
        return ((self.RATIO_WALK_1 * self.weight + ((self.get_mean_speed()
                 * self.COEF_SPEED) ** 2 / (self.height / self.COEF_HEIGHT))
                 * self.RATIO_WALK_2 * self.weight) * (self.duration * 60))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    # Константа длины гребка.
    RATIO_SWIM_1: float = 1.1
    # Коэффициент для подсчета калорий в плавании № 1.
    RATIO_SWIM_2: int = 2
    # Коэффициент для подсчета калорий в плавании № 2.

    """Конструктор дочернего класса - плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Собственный метод дочернего класса для подсчета скорости."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Собственный метод дочернего класса для подсчета калории."""
        multip_data = self.RATIO_SWIM_2 * self.weight * self.duration
        amount_data = self.get_mean_speed() + self.RATIO_SWIM_1
        return amount_data * multip_data


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_workout: dict[str, type[Training]] = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking, }
    if workout_type in dict_workout:
        return dict_workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
