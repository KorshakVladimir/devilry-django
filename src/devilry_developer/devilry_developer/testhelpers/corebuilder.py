from django.contrib.auth.models import User
from datetime import datetime
from datetime import timedelta

from devilry.apps.core.models import Node
from devilry.apps.core.models import Subject
from devilry.apps.core.models import Period
from devilry.apps.core.models import Assignment
from devilry.apps.core.models import AssignmentGroup
from devilry.apps.core.models import Deadline
from devilry.apps.core.models import Delivery
from devilry.apps.core.models import FileMeta

from .datebuilder import DateTimeBuilder


class ReloadableDbBuilderInterface(object):
    def update(self, **attributes):
        raise NotImplementedError()

    def reload_from_db(self):
        raise NotImplementedError()


class UserBuilder(ReloadableDbBuilderInterface):
    def __init__(self, username, full_name=None, email=None):
        email = email or u'{}@example.com'.format(username)
        self.user = User(username=username, email=email)
        self.user.set_password('test')
        self.user.full_clean()
        self.user.save()
        if full_name:
            profile = self.user.get_profile()
            profile.full_name = full_name
            profile.save()

    def update(self, **attributes):
        for attrname, value in attributes.iteritems():
            setattr(self.user, attrname, value)
        self.user.save()
        self.reload_from_db()

    def update_profile(self, **attributes):
        profile = self.user.get_profile()
        for attrname, value in attributes.iteritems():
            setattr(profile, attrname, value)
        profile.save()
        self.reload_from_db()

    def reload_from_db(self):
        self.user = User.objects.get(id=self.user.id)



class CoreBuilderBase(ReloadableDbBuilderInterface):
    object_attribute_name = None

    def _save(self):
        getattr(self, self.object_attribute_name).save()

    def update(self, **attributes):
        for attrname, value in attributes.iteritems():
            setattr(self.node, attrname, value)
        self._save()
        self.reload_from_db()

    def reload_from_db(self):
        obj = getattr(self, self.object_attribute_name)
        setattr(self, self.object_attribute_name, obj.__class__.objects.create(pk=obj.pk))


class BaseNodeBuilderBase(CoreBuilderBase):
    modelcls = None

    def __init__(self, short_name, long_name=None, **kwargs):
        full_kwargs = {
            'short_name': short_name,
            'long_name': long_name or short_name
        }
        full_kwargs.update(kwargs)
        setattr(self, self.object_attribute_name, self.modelcls.objects.create(**full_kwargs))



class FileMetaBuilder(CoreBuilderBase):
    def __init__(self, delivery, filename, data):
        self.filemeta = FileMeta.objects.create(delivery, filename=filename, size=0)
        f = FileMeta.deliverystore.write_open(self.filemeta)
        f.write(data)
        f.close()
        self.filemeta.size = len(data)
        self.filemeta.save()


class DeliveryBuilder(CoreBuilderBase):
    def __init__(self, **kwargs):
        if not 'time_of_delivery' in kwargs:
            kwargs['time_of_delivery'] = datetime.now()
        self.delivery = Delivery.objects.create(**kwargs)

    def _save(self):
        self.delivery.save(autoset_time_of_delivery=False)

    def add_filemeta(self, **kwargs):
        kwargs['delivery'] = self.delivery
        return FileMetaBuilder(**kwargs)


class DeadlineBuilder(CoreBuilderBase):
    def __init__(self, **kwargs):
        self.deadline = Deadline.objects.create(**kwargs)

    def add_delivery(self, **kwargs):
        kwargs['deadline'] = self.deadline
        return DeliveryBuilder(**kwargs)

    def add_delivery_after_deadline(self, timedeltaobject, **kwargs):
        if 'time_of_delivery' in kwargs:
            raise ValueError('add_delivery_after_deadline does not accept ``time_of_delivery`` as kwarg, it sets it automatically.')
        kwargs['time_of_delivery'] = self.deadline.deadline + timedeltaobject
        return self.add_delivery(**kwargs)

    def add_delivery_before_deadline(self, timedeltaobject, **kwargs):
        if 'time_of_delivery' in kwargs:
            raise ValueError('add_delivery_before_deadline does not accept ``time_of_delivery`` as kwarg, it sets it automatically.')
        kwargs['time_of_delivery'] = self.deadline.deadline - timedeltaobject
        return self.add_delivery(**kwargs)

    def add_delivery_x_hours_after_deadline(self, hours, **kwargs):
        self.add_delivery_after_deadline(timedelta(hours=hours))

    def add_delivery_x_hours_before_deadline(self, hours, **kwargs):
        self.add_delivery_before_deadline(timedelta(hours=hours))


class AssignmentGroupBuilder(CoreBuilderBase):
    def __init__(self, students=[], candidates=[], examiners=[], **kwargs):
        self.group = AssignmentGroup.objects.create(**kwargs)
        self.add_students(*students)
        self.add_candidates(*candidates)
        self.add_examiners(*examiners)

    def add_students(self, *users):
        for user in users:
            self.group.candidates.create(student=user)
        return self

    def add_candidates(self, *candidates):
        for candidate in candidates:
            self.group.candidates.add(candidate)
        return self

    def add_examiners(self, *users):
        for user in users:
            self.group.examiners.create(user=user)
        return self

    def add_deadline(self, **kwargs):
        kwargs['assignment_group'] = self.group
        return DeadlineBuilder(**kwargs)

    def add_deadline_in_x_weeks(self, weeks, **kwargs):
        if 'deadline' in kwargs:
            raise ValueError('add_deadline_in_x_weeks does not accept ``deadline`` as kwarg, it sets it automatically.')
        kwargs['deadline'] = DateTimeBuilder.now().plus(weeks=weeks)
        return self.add_deadline(**kwargs)

    def add_deadline_x_weeks_ago(self, weeks, **kwargs):
        if 'deadline' in kwargs:
            raise ValueError('add_deadline_x_weeks_ago does not accept ``deadline`` as kwarg, it sets it automatically.')
        kwargs['deadline'] = DateTimeBuilder.now().minus(weeks=weeks)
        return self.add_deadline(**kwargs)


class AssignmentBuilder(BaseNodeBuilderBase):
    object_attribute_name = 'assignment'
    modelcls = Assignment

    def __init__(self, *args, **kwargs):
        if not 'publishing_time' in kwargs:
            kwargs['publishing_time'] = datetime.now()
        super(AssignmentBuilder, self).__init__(*args, **kwargs)

    def add_group(self, *args, **kwargs):
        kwargs['parentnode'] = self.assignment
        return AssignmentGroupBuilder(*args, **kwargs)



class PeriodBuilder(BaseNodeBuilderBase):
    object_attribute_name = 'period'
    modelcls = Period


    @classmethod
    def quickadd_ducku_duck1010_current(cls):
        return SubjectBuilder.quickadd_ducku_duck1010().add_6month_active_period('current')

    def add_assignment(self, *args, **kwargs):
        kwargs['parentnode'] = self.period
        return AssignmentBuilder(*args, **kwargs)


class SubjectBuilder(BaseNodeBuilderBase):
    object_attribute_name = 'subject'
    modelcls = Subject

    @classmethod
    def quickadd_ducku_duck1010(cls):
        return NodeBuilder('ducku').add_subject('duck1010')

    def add_period(self, *args, **kwargs):
        kwargs['parentnode'] = self.subject
        return PeriodBuilder(*args, **kwargs)

    def add_6month_active_period(self, *args, **kwargs):
        kwargs['parentnode'] = self.subject
        if 'start_time' in kwargs or 'end_time' in kwargs:
            raise ValueError('add_6month_active_period does not accept ``start_time`` or ``end_time`` as kwargs, it sets them automatically.')
        kwargs['start_time'] = DateTimeBuilder.now().minus(days=30*3)
        kwargs['end_time'] = DateTimeBuilder.now().plus(days=30*3)
        return self.add_period(*args, **kwargs)

    def add_6month_lastyear_period(self, *args, **kwargs):
        kwargs['parentnode'] = self.subject
        if 'start_time' in kwargs or 'end_time' in kwargs:
            raise ValueError('add_6month_lastyear_period does not accept ``start_time`` or ``end_time`` as kwargs, it sets them automatically.')
        kwargs['start_time'] = DateTimeBuilder.now().minus(days=365 - 30*3)
        kwargs['end_time'] = DateTimeBuilder.now().minus(days=365 + 30*3)
        return self.add_period(*args, **kwargs)

    def add_6month_nextyear_period(self, *args, **kwargs):
        kwargs['parentnode'] = self.subject
        if 'start_time' in kwargs or 'end_time' in kwargs:
            raise ValueError('add_6month_nextyear_period does not accept ``start_time`` or ``end_time`` as kwargs, it sets them automatically.')
        kwargs['start_time'] = DateTimeBuilder.now().plus(days=365 - 30*3)
        kwargs['end_time'] = DateTimeBuilder.now().plus(days=365 + 30*3)
        return self.add_period(*args, **kwargs)


class NodeBuilder(BaseNodeBuilderBase):
    object_attribute_name = 'node'
    modelcls = Node

    def add_subject(self, *args, **kwargs):
        kwargs['parentnode'] = self.node
        return SubjectBuilder(*args, **kwargs)
