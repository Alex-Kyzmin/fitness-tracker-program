class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: float,
                 distance: float, speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Cообщение о тренировке."""
        message = (
            f'Тип тренировки: {self.training_type};'
            f' Длительность: {self.duration:.3f} ч.;'
            f' Дистанция: {self.distance:.3f} км;'
            f' Ср. скорость: {self.speed:.3f} км/ч;'
            f' Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    # Константы базового класса.
    LEN_STEP: float = 0.65  # Длина шага при беге или ходьбе.
    M_IN_KM: int = 1000  # Коэффициент перевода значений из метров в километры.
    COEF_MIN: int = 60  # Коэффициент перевода значений из часов в минуты.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        """Конструктор базового класса."""

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type, self.duration,
                           distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""
    # Константы дочернего класса.
    CALORIES_MEAN_SPEED_MULTIP = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Собственный метод дочернего класса для подсчета калории."""
        return ((self.CALORIES_MEAN_SPEED_MULTIP * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * (self.duration * Training.COEF_MIN))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # Константы дочернего класса.
    RATIO_WALK_1: float = 0.035
    # Коэффициент для подсчета калорий при ходьбе № 1.
    RATIO_WALK_2: float = 0.029
    # Коэффициент для подсчета калорий при ходьбе № 2.
    COEF_SPEED: float = 0.278
    # Коэффициент превода из км/ч в м/с.
    COEF_HEIGHT: int = 100
    # Коэффициент превода см в м.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        """Конструктор дочернего класса."""

    def get_spent_calories(self) -> float:
        """Собственный метод дочернего класса для подсчета калории."""
        return ((self.RATIO_WALK_1 * self.weight + ((self.get_mean_speed()
                 * self.COEF_SPEED) ** 2 / (self.height / self.COEF_HEIGHT))
                 * self.RATIO_WALK_2 * self.weight) * (self.duration * 60))


class Swimming(Training):
    """Тренировка: плавание."""
    # Константы дочернего класса.
    LEN_STEP: float = 1.38
    RATIO_SWIM_1: float = 1.1
    # Коэффициент для подсчета калорий в плавании № 1.
    RATIO_SWIM_2: int = 2
    # Коэффициент для подсчета калорий в плавании № 2.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool
        """Конструктор базового класса."""

    def get_mean_speed(self) -> float:
        """Собственный метод дочернего класса для подсчета скорости."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Собственный метод дочернего класса для подсчета калории."""
        return (self.get_mean_speed() + self.RATIO_SWIM_1
                ) * self.RATIO_SWIM_2 * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in dict_workout:
        return dict_workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
