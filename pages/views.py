from django.shortcuts import render
from django.views.generic import TemplateView, View
from pages.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
import smtplib
from django.views.decorators.csrf import requires_csrf_token
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
import datetime



class AuthView(TemplateView):
    template_name = 'page/login.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        else:
            if request.user.is_teacher:
                return HttpResponseRedirect('/teacher')
            elif request.user.is_superuser:
                return HttpResponseRedirect('/admin')

            return HttpResponseRedirect('/child')

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    print('logged')
                    if user.is_teacher:
                        return HttpResponseRedirect('/')
                    elif user.is_superuser:
                        return HttpResponseRedirect('/')
                    return HttpResponseRedirect('/')
        else:
            if request.user.is_superuser:
                return HttpResponseRedirect('/admin')
            elif request.user.is_teacher:
                return HttpResponseRedirect('/teacher')
            return HttpResponseRedirect('/child')

        return HttpResponseRedirect('/book')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')


class TeacherPageView(TemplateView):
    template_name = 'page/index.html'
    check_first = True

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['mark'] = '4,6'
        ctx['schools'] = School.objects.all()
        ctx['schoolSubjects'] = SchoolSubject.objects.all()
        ctx['groups'] = Group.objects.all()
        ctx['users'] = User.objects.all()
        ctx['lessons'] = Lesson.objects.all()
        ctx['marks'] = Mark.objects.all()
        ctx['checkFirst'] = False
        # ctx['students'] = self.get_queryset()
        return ctx

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_teacher:
            self.school_id = request.GET.get('school_id')
            self.lesson_id = request.GET.get('lesson_id')
            self.group_id = request.GET.get('group_id')
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/admin')


class ChildPageView(TemplateView):
    template_name = 'page/child.html'
    check_first = True

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser == False and request.user.is_teacher == False:
            use = User.objects.filter(id=request.user.id).first()
            self.subjects = SchoolSubject.objects.filter(school__id=use.subgroup.group.school.id).all()
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['subjects'] = self.subjects
        ctx['checkFirst'] = False
        return ctx


class SetLessonView(View):
    def get(self, request, *args, **kwargs):
        if (request.user.is_teacher or request.user.is_superuser) or (request.user.is_teacher and request.user.is_superuser):
            subgr_id = request.GET.get('subgroupid')
            subject_id = request.GET.get('subid')
            date = request.GET.get('date')

            if subgr_id is not None and subject_id is not None and date is not None:
                if Day.objects.filter(date=date).first():
                    day = Day.objects.filter(date=date).first()
                else:
                    day = Day.objects.create(date=date)

                if Lesson.objects.filter(teacher__id=request.user.id, students__id=subgr_id, date=day, subject__id=subject_id).first():
                    return JsonResponse(['already'], safe=False)
                else:
                    user = User.objects.filter(id=request.user.id).first()
                    subgroup = SubGroup.objects.filter(id=subgr_id).first()
                    subject = SchoolSubject.objects.filter(id=subject_id).first()
                    lesson = Lesson.objects.create(teacher=user, students=subgroup, date=day, subject=subject)
                    return JsonResponse(['create'], safe=False)
        return JsonResponse(['bad'], safe=False)


class SetMarkView(View):
    def get(self, request, *args, **kwargs):
        if (request.user.is_teacher or request.user.is_superuser) or (request.user.is_teacher and request.user.is_superuser):
            user_id = request.GET.get('userid')
            mark_id = request.GET.get('markid')
            lesson_id = request.GET.get('lessonid')
            mark_val = request.GET.get('markval')

            if lesson_id is not None and user_id is not None and mark_id is not None and mark_val is not None:
                user = User.objects.filter(id=user_id).first()
                lesson = Lesson.objects.filter(id=lesson_id).first()
                if mark_id == 'undefined' and mark_val != 'none':
                    mark = Mark.objects.create(student=user, lesson=lesson, mark=mark_val)
                    return JsonResponse([{
                        'answer': 'create',
                        'mark_id': mark.id
                        }], safe=False)
                elif mark_id != 'undefined' and mark_val != 'none':
                    mark = Mark.objects.filter(id=mark_id).first()
                    mark.mark = mark_val
                    mark.save()
                    return JsonResponse(['change'], safe=False)
                elif mark_val == 'none':
                    Mark.objects.filter(id=mark_id).delete()
                    return JsonResponse(['delete'], safe=False)
        return JsonResponse(['bad'], safe=False)


class PeriodApiView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            subject_id = request.GET.get('subjectid')
            subgroup_id = request.GET.get('subgroupid')
            if subject_id is not None and subgroup_id is not None:
                period = Period.objects.filter(subject__id=subject_id, students__id=subgroup_id).first()
                if period is not None:
                    return JsonResponse([
                        {
                            'id': period.id,
                            'name': period.name,
                        }
                    ], safe=False)
        return JsonResponse(['bad'], safe=False)


class MarkApiView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_id = request.GET.get('userid')
            lesson_id = request.GET.get('lessonid')
            if lesson_id is not None and user_id is not None:
                mark = Mark.objects.filter(student__id=user_id, lesson__id=lesson_id).first()
                if mark is not None:
                    # mark_choice = LessonResultEnum.get_value(mark.mark)
                    return JsonResponse([
                        {
                            'id': mark.id,
                            'markchoice': mark.mark,
                            'userid': user_id
                        }
                    ], safe=False)
        return JsonResponse(['bad'], safe=False)


class TableApiView(View):
    def get(self, request, *args, **kwargs):
        school_id = request.GET.get('schoolid')
        group_id = request.GET.get('groupid')
        period_name = request.GET.get('periodname')
        child = request.GET.get('child')


        period = Period.objects.filter(id=period_name).first()

        if (child == 'true') and (period is not None) and request.user.is_authenticated:
            lesson = Lesson.objects.filter( subject__id=period.subject.id, students__id=request.user.subgroup.id, date__date__gte=period.date_from.date, date__date__lt=period.date_to.date).all().order_by('-date')
            if lesson:
                return JsonResponse([{
                    "id": les.id,
                    "date": les.date.date,
                    "subject": les.subject.name,
                    "mark": LessonResultEnum.get_value(Mark.objects.filter(student__id=request.user.id, lesson__id=les.id).first().mark)
                } for les in lesson], safe=False)
            else:
                return JsonResponse(['bad'], safe=False)
        elif (school_id != 'null') and (group_id != 'null') and (period is not None) and ((request.user.is_teacher or request.user.is_superuser) or (request.user.is_teacher and request.user.is_superuser)):
            users = User.objects.filter(subgroup__id=period.students.id).all()
            lessons = Lesson.objects.filter( subject__id=period.subject.id, students__id=period.students.id, date__date__gte=period.date_from.date, date__date__lt=period.date_to.date).all().order_by('-date')
            if users and lessons:
                return JsonResponse({
                "user":[{
                    'id': x.id,
                    'first_name': x.first_name,
                    'last_name': x.last_name
                } for x in users], 
                "lesson":[{
                    "id": les.id,
                    "teacher_name": les.teacher.first_name,
                    "teacher_lastname": les.teacher.last_name,
                    "date": les.date.date,
                    "subject": les.subject.name
                } for les in lessons]}, safe=False)
            else:
                return JsonResponse(['bad'], safe=False)
        return JsonResponse(['bad'], safe=False)


class SubGroupsApiView(View):
    def get(self, request, *args, **kwargs):
        if (request.user.is_teacher or request.user.is_superuser) or (request.user.is_teacher and request.user.is_superuser):
            group_id = request.GET.get('id')
            if group_id is not None:
                group = Group.objects.filter(id=group_id).first()
                if group is not None:
                    return JsonResponse([
                        {
                            'id': x.id,
                            'name': x.index
                        }
                     for x in group.subgroups.all()], safe=False)
        return JsonResponse(['bad'], safe=False)


class GroupsApiView(View):
    def get(self, request, *args, **kwargs):
        if (request.user.is_teacher or request.user.is_superuser) or (request.user.is_teacher and request.user.is_superuser):
            school_id = request.GET.get('id')
            if school_id is not None:
                school = School.objects.filter(id=school_id).first()
                if school is not None:
                    return JsonResponse([
                        {
                            'id': x.id,
                            'name': x.name
                        }
                     for x in school.groups.all()], safe=False)
        return JsonResponse(['bad'], safe=False)


class SubjectsApiView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            school_id = request.GET.get('id')
            if school_id is not None:
                school = School.objects.filter(id=school_id).first()
                if school is not None:
                    return JsonResponse([
                        {
                            'id': x.id,
                            'name': x.name
                        }
                     for x in school.subjects.all()], safe=False)
        return JsonResponse(['bad'], safe=False)

 

