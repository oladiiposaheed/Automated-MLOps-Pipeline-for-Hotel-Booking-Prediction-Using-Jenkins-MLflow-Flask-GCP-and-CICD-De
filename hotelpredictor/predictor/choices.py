month_lists = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

MONTH_CHOICES = [(i, month) for i, month in enumerate(month_lists, 1)]

DATE_CHOICES = [(i, i) for i in range(1, 32)]

MARKET_SEGMENT_CHOICES = [
    (0, 'Aviation'),
    (1, 'Complementary'),
    (2, 'Corperate'),
    (3, 'Offline'),
    (4, 'Online')
]

MEAL_PLAN_CHOICES = [
    (0, 'Meal Plan 1'),
    (1, 'Meal Plan 2'),
    (2, 'Meal Plan 3'),
    (4, 'Not Selected')
]

ROOM_TYPE_CHOICES = [(i, f'Room Type {i + 1}') for i in range(7)]
