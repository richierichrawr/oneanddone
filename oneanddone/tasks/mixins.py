# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.core.exceptions import PermissionDenied

from oneanddone.tasks.models import Task


class TaskMustBePublishedMixin(object):
    """
    Only allow published tasks to be accessed, by filtering the
    queryset.
    """
    allow_expired_tasks = False

    def get_queryset(self):
        queryset = super(TaskMustBePublishedMixin, self).get_queryset()
        return queryset.filter(Task.is_available_filter(allow_expired=self.allow_expired_tasks))


class APIRecordCreatorMixin(object):
    def pre_save(self, obj):
        obj.creator = self.request.user


class APIOnlyCreatorMayDeleteMixin(object):
    def pre_delete(self, obj):
        if obj.creator != self.request.user:
            raise PermissionDenied()
