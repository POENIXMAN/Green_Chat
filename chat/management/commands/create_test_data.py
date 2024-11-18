import random
from django.core.management.base import BaseCommand
from chat.models import User, Channel, Message
from faker import Faker

class Command(BaseCommand):
    help = "Create test data for chat application"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Создание пользователей
        self.stdout.write("Creating users...")
        for _ in range(10):
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="12345"
            )

        users = list(User.objects.all())

        # Создание каналов
        self.stdout.write("Creating channels...")
        for i in range(5):
            channel = Channel.objects.create(
                name=f"Test Channel {i+1}"
            )
            # Добавляем случайных пользователей в канал
            channel.users.add(*random.sample(users, random.randint(2, len(users))))

        channels = list(Channel.objects.all())

        # Создание сообщений
        self.stdout.write("Creating messages...")
        for _ in range(100):
            Message.objects.create(
                sender=random.choice(users),
                channel=random.choice(channels),
                text=fake.sentence(),
            )

        self.stdout.write(self.style.SUCCESS("Test data created successfully!"))
