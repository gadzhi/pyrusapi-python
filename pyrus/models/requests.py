from datetime import datetime
from . import entities

DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DATE_FORMAT = '%Y-%m-%d'

class FormRegisterRequest(object):
    def __init__(self, steps=None, include_archived=False, filters=None, modified_before=None, modified_after=None):
        if steps:
            if not isinstance(steps, list):
                raise TypeError('steps must be a list of int')
            for item in steps:
                if not isinstance(item, int):
                    raise TypeError('steps must be a list of int')
            self.steps = steps

        if not isinstance(include_archived, bool):
            raise TypeError('include_archived must be bool')
        self.include_archived = include_archived

        if modified_before:
            if not isinstance(modified_before, datetime):
                raise TypeError('modified_before must be a date')
            self.modified_before = datetime.strftime(modified_before, DATE_TIME_FORMAT)

        if modified_after:
            if not isinstance(modified_after, datetime):
                raise TypeError('modified_after must be a date')
            self.modified_after = datetime.strftime(modified_after, DATE_TIME_FORMAT)

        if filters:
            if not isinstance(filters, list):
                raise TypeError('filters must be a list of entities.FormRegisterFilter')
            for fltr in filters:
                if not isinstance(fltr, entities.FormRegisterFilter):
                    raise TypeError('filters must be a list of entities.FormRegisterFilter')
                if fltr.operator == 'equals':
                    setattr(self, 'fld{}'.format(fltr.field_id), fltr.values)
                if fltr.operator == 'greater_than':
                    setattr(self, 'fld{}'.format(fltr.field_id), 'gt{}'.format(fltr.values))
                if fltr.operator == 'less_than':
                    setattr(self, 'fld{}'.format(fltr.field_id), 'lt{}'.format(fltr.values))
                if fltr.operator == 'range':
                    setattr(self, 'fld{}'.format(fltr.field_id), 'gt{},lt{}'.format(*fltr.values))
                if fltr.operator == 'is_in':
                    setattr(self, 'fld{}'.format(fltr.field_id), ",".join(fltr.values))

class TaskCommentRequest(object):
    def __init__(self, text=None, approval_choice=None, approval_steps=None, action=None,
                 attachments=None, field_updates=None, approvals_added=None,
                 participants_added=None, reassign_to=None, due=None,
                 due_date=None, duration=None, scheduled_date=None,
                 cancel_schedule=None, added_list_ids=None, removed_list_ids=None,
                 approvals_removed=None, approvals_rerequested=None, subject = None):
        self.text = text
        self.subject = subject
        if approval_choice:
            if approval_choice not in ['approved', 'rejected', 'revoked', 'acknowledged']:
                raise TypeError('approval_choice can only be \'approved\', \'rejected\', \'acknowledged\', or \'revoked\'')
            self.approval_choice = approval_choice
        if action:
            if action not in ['finished', 'reopened']:
                raise TypeError('action can only be \'finished\' or \'reopened\'')
            self.action = action
        if reassign_to:
            if isinstance(reassign_to, entities.Person):
                self.reassign_to = reassign_to
            elif isinstance(reassign_to, int):
                self.reassign_to = entities.Person(id=reassign_to)
            else:
                self.reassign_to = entities.Person(email=reassign_to)
        if attachments:
            if not isinstance(attachments, list):
                raise TypeError('attachments must be a list of guids')
            self.attachments = []
            for attachment in attachments:
                self.attachments.append(attachment)
        if approvals_added:
            if not isinstance(approvals_added, list):
                raise TypeError('approvals_added must be a list')
            self.approvals_added = []
            for idx, approval_step in enumerate(approvals_added):
                if not isinstance(approval_step, list):
                    raise TypeError('approval_step must be a list of persons, person ids'
                                    ', or person emails')
                self.approvals_added.append([])
                for person in approval_step:
                    if isinstance(person, entities.Person):
                        self.approvals_added[idx].append(person)
                    elif isinstance(person, int):
                        self.approvals_added[idx].append(entities.Person(id=person))
                    else:
                        self.approvals_added[idx].append(entities.Person(email=person))
        if approvals_removed:
            if not isinstance(approvals_removed, list):
                raise TypeError('approvals_removed must be a list')
            self.approvals_removed = []
            for idx, approval_step in enumerate(approvals_removed):
                if not isinstance(approval_step, list):
                    raise TypeError('approval_step must be a list of persons, person ids'
                                    ', or person emails')
                self.approvals_removed.append([])
                for person in approval_step:
                    if isinstance(person, entities.Person):
                        self.approvals_removed[idx].append(person)
                    elif isinstance(person, int):
                        self.approvals_removed[idx].append(entities.Person(id=person))
                    else:
                        self.approvals_removed[idx].append(entities.Person(email=person))
        if approvals_rerequested:
            if not isinstance(approvals_rerequested, list):
                raise TypeError('approvals_rerequested must be a list')
            self.approvals_rerequested = []
            for idx, approval_step in enumerate(approvals_rerequested):
                if not isinstance(approval_step, list):
                    raise TypeError('approval_step must be a list of persons, person ids'
                                    ', or person emails')
                self.approvals_rerequested.append([])
                for person in approval_step:
                    if isinstance(person, entities.Person):
                        self.approvals_rerequested[idx].append(person)
                    elif isinstance(person, int):
                        self.approvals_rerequested[idx].append(entities.Person(id=person))
                    else:
                        self.approvals_rerequested[idx].append(entities.Person(email=person))
        if participants_added:
            if not isinstance(participants_added, list):
                raise TypeError('participants_added must be a list')
            self.participants_added = []
            for person in participants_added:
                try:
                    int(person)
                    self.participants_added.append(entities.Person(id=person))
                except ValueError:
                    self.participants_added.append(entities.Person(email=person))
        if field_updates:
            self.field_updates = []
            for field_update in field_updates:
                if isinstance(field_update, entities.FormField):
                    self.field_updates.append(field_update)
                else:
                    if 'name' not in field_update and 'id' not in field_update:
                        raise TypeError('each field_update in field_updates '
                                        'must contain field id or name')
                    if 'value' not in field_update:
                        raise TypeError('each field_update in field_updates must '
                                        'contain field value')
                    self.field_updates.append(field_update)
        if due_date:
            if not isinstance(due_date, datetime):
                raise TypeError('due_date must be a date')
            self.due_date = datetime.strftime(due_date, DATE_FORMAT)
        if due:
            if not isinstance(due, datetime):
                raise TypeError('due must be a date')
            self.due = datetime.strftime(due, DATE_TIME_FORMAT)
        if duration:
            if not isinstance(due, int):
                raise TypeError('duration must be an int')
            self.duration = duration
        if scheduled_date:
            if not isinstance(scheduled_date, datetime):
                raise TypeError('scheduled_date must be a date')
            self.scheduled_date = datetime.strftime(scheduled_date, DATE_FORMAT)
        if cancel_schedule:
            if not isinstance(cancel_schedule, bool):
                raise TypeError('cancel_schedule must be a bool')
            self.cancel_schedule = datetime.strftime(cancel_schedule, DATE_FORMAT)
        if added_list_ids:
            if not isinstance(added_list_ids, list):
                raise TypeError('added_list_ids must be a list of int')
            for item in added_list_ids:
                if not isinstance(item, int):
                    raise TypeError('added_list_ids must be a list of int')
            self.added_list_ids = added_list_ids
        if removed_list_ids:
            if not isinstance(removed_list_ids, list):
                raise TypeError('removed_list_ids must be a list of int')
            for item in removed_list_ids:
                if not isinstance(item, int):
                    raise TypeError('removed_list_ids must be a list of int')
            self.removed_list_ids = removed_list_ids
        if approval_steps:
            if not isinstance(approval_steps, list):
                raise TypeError('approval_steps must be a list of int')
            for item in approval_steps:
                if not isinstance(item, int):
                    raise TypeError('approval_steps must be a list of int')
            self.approval_steps = approval_steps

class CreateTaskRequest(object):
    def __init__(self, text=None, subject=None, parent_task_id=None,
                 due_date=None, form_id=None, attachments=None, responsible=None,
                 fields=None, approvals=None, participants=None, list_ids=None,
                 due=None, duration=None, scheduled_date=None, fill_defaults = None):
        if text:
            self.text = text
        if subject:
            self.subject = subject
        if parent_task_id:
            if not isinstance(parent_task_id, int):
                raise TypeError('parent_task_id must be an int')
            self.parent_task_id = parent_task_id
        if due_date:
            if not isinstance(due_date, datetime):
                raise TypeError('due_date must be a date')
            self.due_date = datetime.strftime(due_date, DATE_FORMAT)
        if due:
            if not isinstance(due, datetime):
                raise TypeError('due must be a date')
            self.due = datetime.strftime(due, DATE_TIME_FORMAT)
        if duration:
            if not isinstance(duration, int):
                raise TypeError('duration must be an int')
            self.duration = duration
        if scheduled_date:
            if not isinstance(scheduled_date, datetime):
                raise TypeError('scheduled_date must be a date')
            self.scheduled_date = datetime.strftime(scheduled_date, DATE_FORMAT)
        if form_id:
            if not isinstance(form_id, int):
                raise TypeError('form_id must be int')
            self.form_id = form_id
        if attachments:
            if not isinstance(attachments, list):
                raise TypeError('attachments must be a list of guids')
            self.attachments = []
            for attachment in attachments:
                self.attachments.append(attachment)
        if responsible:
            if isinstance(responsible, entities.Person):
                self.responsible = responsible
            elif isinstance(responsible, int):
                self.responsible = entities.Person(id=responsible)
            else:
                self.responsible = entities.Person(email=responsible)
        if fields:
            self.fields = []
            for field in fields:
                if isinstance(field, entities.FormField):
                    self.fields.append(field)
                else:
                    if 'name' not in field and 'id' not in field:
                        raise TypeError('each field in fields '
                                        'must contain field id or name')
                    if 'value' not in field:
                        raise TypeError('each field in fields must '
                                        'contain field value')
                    self.fields.append(field)
        if approvals:
            if not isinstance(approvals, list):
                raise TypeError('approvals must be a list')
            self.approvals = []
            for idx, approval_step in enumerate(approvals):
                if not isinstance(approval_step, list):
                    raise TypeError('approval_step must be a list of persons, person ids'
                                    ', or person emails')
                self.approvals.append([])
                for person in approval_step:
                    if isinstance(person, entities.Person):
                        self.approvals[idx].append(person)
                    elif isinstance(person, int):
                        self.approvals[idx].append(entities.Person(id=person))
                    else:
                        self.approvals[idx].append(entities.Person(email=person))
        if participants:
            if not isinstance(participants, list):
                raise TypeError('approvals_added must be a list')
            self.participants = []
            for person in participants:
                try:
                    int(person)
                    self.participants.append(entities.Person(id=person))
                except ValueError:
                    self.participants.append(entities.Person(email=person))
        if list_ids:
            if not isinstance(list_ids, list):
                raise TypeError('list_ids must be a list of int')
            for item in list_ids:
                if not isinstance(item, int):
                    raise TypeError('list_ids must be a list of int')
            self.list_ids = list_ids
        if fill_defaults:
            if not isinstance(fill_defaults, bool):
                raise TypeError("fill_defaults must be a boolean")
            self.fill_defaults = fill_defaults

class SyncCatalogRequest(object):
    def __init__(self, apply=None, catalog_headers=None, items=None):
        if apply:
            if not isinstance(apply, bool):
                raise TypeError('apply must be a bool')
            self.apply = apply
        if catalog_headers:
            _validata_catalog_headers(catalog_headers)
            self.catalog_headers = catalog_headers
        if items:
            self.items = _get_catalog_items(items)

class CreateCatalogRequest(object):
    def __init__(self, name=None, catalog_headers=None, items=None):
        if name:
            if not isinstance(name, str):
                raise TypeError('name must be a str')
            self.name = name
        if catalog_headers:
            _validata_catalog_headers(catalog_headers)
            self.catalog_headers = catalog_headers
        if items:
            self.items = _get_catalog_items(items)

def _validata_catalog_headers(catalog_headers):
    if not isinstance(catalog_headers, list):
        raise TypeError('catalog_headers must be a list of str')
    for item in catalog_headers:
        if not isinstance(item, str):
            raise TypeError('list_ids must be a list of str')

def _get_catalog_items(catalog_items):
    if not isinstance(catalog_items, list):
        raise TypeError('catalog_items must be a list')
    
    items = []
    for item in catalog_items:
        try:
            items.append(entities.CatalogItem.fromliststr(item))
        except TypeError:
            if not isinstance(item, entities.CatalogItem):
                raise TypeError('catalog_items must be a list of CatalogItems')
            items.append(item)
    return items
