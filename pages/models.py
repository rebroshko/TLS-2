from django.db import models
from django.contrib.auth.models import AbstractUser

from pages.utils import BaseEnum


class LessonResultEnum(BaseEnum):
    A = "5"
    B = "4"
    C = "3"
    D = "2"
    E = "1"
    UNATTENDED = "UNATTENDED"
    ILL = "ILL"


class Day(models.Model):
    date = models.DateField(verbose_name="Дата")

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'Дни'


class School(models.Model):
    address = models.TextField(verbose_name="Адрес")

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'


class SchoolSubject(models.Model):
    name = models.TextField(verbose_name="Название")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="subjects", verbose_name="Школа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Group(models.Model):
    name = models.TextField(verbose_name="Название")
    course = models.IntegerField(verbose_name="Курс")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="groups")

    def __str__(self):
        return f"{self.name} - {self.school}"

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class SubGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="subgroups", verbose_name="Группа")

    @property
    def index(self):
        return self.group.subgroups.filter(id__lt=self.id).count() + 1
    
    def __str__(self):
        return f"{str(self.group.name)}: {str(self.index)} подгруппа"

    class Meta:
        verbose_name = 'Подгруппа'
        verbose_name_plural = 'Подгруппы'


class User(AbstractUser):
    subgroup = models.ForeignKey(SubGroup, null=True, blank=True, on_delete=models.CASCADE, related_name="students", verbose_name="Подгруппа")
    first_name = models.TextField(null=True, blank=True, verbose_name="Имя")
    last_name = models.TextField(null=True, blank=True, verbose_name="Фамилия")
    age = models.IntegerField(null=True, blank=True, verbose_name="Возраст")
    is_teacher = models.BooleanField(default=False, verbose_name="Права учителя")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        group = str(self.subgroup.group) if self.subgroup else ""
        status = "Teacher" if self.is_teacher else f"Student {group}"
        return f"{status} - {self.get_full_name()}"

        if self.is_teacher:
            self.subgroup = None
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Lesson(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons_from_teacher", verbose_name="Учитель")
    students = models.ForeignKey(SubGroup, on_delete=models.CASCADE, related_name="lessons_of_subgroup", verbose_name="Подгруппа")
    date = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="lessons_in_date", verbose_name="Дата")
    subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE, related_name="subject_lessons", verbose_name="Предмет")

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Mark(models.Model):
    mark = models.TextField(choices=LessonResultEnum.get_choices(), verbose_name="Оценка")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_marks", verbose_name="Ученик")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_marks", verbose_name="Урок")

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'



class Period(models.Model):
    name = models.TextField()
    date_from = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="period_in_date_from", verbose_name="Дата от")
    date_to = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="period_in_date_to", verbose_name="Дата до")
    subject = models.ForeignKey(SchoolSubject, on_delete=models.CASCADE, related_name="subject_period", verbose_name="Предмет")
    students = models.ForeignKey(SubGroup, on_delete=models.CASCADE, related_name="students_of_period", verbose_name="Подгруппа")

    class Meta:
        verbose_name = 'Период'
        verbose_name_plural = 'Периоды'
