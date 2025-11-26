import time
from random import choices, random, randint
from contextlib import contextmanager

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from app.models import (
    User,
    Profile,
    Question,
    Answer,
    Tag,
    QuestionsLikes,
    AnswersLikes,
)

from faker import Faker


class Command(BaseCommand):
    help = "Заполнение база данных синтетическими данными"

    users_count_min = 50

    questions_ratio = 10
    answers_ratio = 100
    likes_ratio = 200
    tags_ratio = 1

    batch_size = 500

    default_password = "fake1234"

    username_min_length = 20
    username_max_length = 30

    question_title_words = 10
    question_text_words = 50
    max_tags_per_question = 3

    answer_text_words = 50
    answer_is_correct_p = 0.8

    like_p = 0.4

    faker = Faker()

    @contextmanager
    def status(self, message):
        self.stdout.write(message, ending=" ")
        self.stdout.flush()

        try:
            start_time = time.time()
            yield
            end_time = time.time()
        except Exception as e:
            self.stdout.write(
                self.style.ERROR("ERROR")
            )
            raise e
        
        self.stdout.write(
            self.style.SUCCESS("OK") + f" {end_time - start_time:.2f}s"
        )

    @staticmethod
    def users_count_validate(value):
        users_count = int(value)

        if users_count < Command.users_count_min:
            raise CommandError(f"Минимальное кол-во пользователей для создания {Command.users_count_min}")
        
        return users_count

    def add_arguments(self, parser):
        parser.add_argument("users_count", type=Command.users_count_validate)

    def _create_profiles(self, users_count):
        users = list()
        profiles = list()

        for _ in range(users_count):
            username = self.faker.unique.pystr(
                min_chars=self.username_min_length,
                max_chars=self.username_max_length
            )
            email = self.faker.email()
            
            user = User(
                username=username,
                email=email,
                password=self.default_password
            )

            users.append(user)
            profiles.append(
                Profile(user=user, nickname=self.faker.user_name())
            )

        User.objects.bulk_create(users, batch_size=self.batch_size)
        return Profile.objects.bulk_create(profiles, batch_size=self.batch_size)
    
    def _create_questions(self, profiles):
        questions = list()

        for profile in profiles:
            for _ in range(self.questions_ratio):
                questions.append(
                    Question(
                        title=self.faker.sentence(nb_words=self.question_title_words),
                        text=self.faker.sentence(nb_words=self.question_text_words),
                        profile=profile,
                    )
                )

        return Question.objects.bulk_create(questions, batch_size=self.batch_size)
    
    def _create_tags(self, tags_count):
        tags = list()

        for i in range(tags_count):
            tags.append(
                Tag(
                    name=f"{self.faker.word()}_{i}"
                )
            )

        return Tag.objects.bulk_create(tags, batch_size=self.batch_size)
    
    def _create_answers(self, questions, profiles):
        answers = list()

        questions_count = len(questions)
        for profile in profiles:
            for _ in range(self.answers_ratio):
                answers.append(
                    Answer(
                        text=self.faker.sentence(nb_words=self.answer_text_words),
                        is_correct=(random() > self.answer_is_correct_p),
                        profile=profile,
                        question=questions[randint(0, questions_count - 1)]
                    )
                )

        return Answer.objects.bulk_create(answers, batch_size=self.batch_size)
    
    def _set_tags(self, questions, tags):
        for question in questions:
            question.tags.set(
                choices(tags, k=(question.id % self.max_tags_per_question + 1))
            )

    def _set_likes_on_questions_and_answers(self, profiles, questions, answers):
        questions_likes = list()
        answers_likes = list()

        questions_count = len(questions)
        answers_count = len(answers)

        for profile in profiles:
            self.faker.unique.clear()

            for _ in range(self.likes_ratio):
                questions_likes.append(
                    QuestionsLikes(
                        profile=profile,
                        question=questions[self.faker.unique.random_int(
                            min=0,
                            max=questions_count - 1
                        )],
                        is_like=(random() > self.like_p)
                    )
                )

                answers_likes.append(
                    AnswersLikes(
                        profile=profile,
                        answer=answers[self.faker.unique.random_int(
                            min=0,
                            max=answers_count - 1
                        )],
                        is_like=(random() > self.like_p)
                    )
                )

        QuestionsLikes.objects.bulk_create(questions_likes, batch_size=self.batch_size)
        AnswersLikes.objects.bulk_create(answers_likes, batch_size=self.batch_size)

    def _write_ok_message(self):
        self.stdout.write(
            self.style.SUCCESS("OK")
        )

    def _write_error_message(self):
        self.stderr.write(
            self.style.ERROR("ERROR")
        )

    def handle(self, *args, **options):
        users_count = options["users_count"]

        with transaction.atomic():
            # Создание пользователей
            with self.status("Создание пользователей..."):
                profiles = self._create_profiles(users_count)

            # Создание вопросов
            with self.status("Создание вопросов..."):
                questions = self._create_questions(profiles)

            # Создание тегов
            with self.status("Создание тегов..."):
                tags = self._create_tags(users_count)

            # Создание ответов
            with self.status("Создание ответов..."):
                answers = self._create_answers(questions, profiles)

            # Устновка тегов на вопросы
            with self.status("Установка тегов на вопросы..."):
                self._set_tags(questions, tags)

            # Установка лайков на вопросы и ответы
            with self.status("Установка лайков на вопросы и ответы..."):
                self._set_likes_on_questions_and_answers(
                    profiles,
                    questions,
                    answers
                )

