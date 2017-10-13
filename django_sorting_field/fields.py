from django import forms
import json

from .widgets import SortingWidget
from .utils import iterate_in_order, clean_order_json


class SortedItem(object):

    def __init__(self, identifier, label):
        self.id = identifier
        self.label = label


class SortingFormField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.update({
            "widget": SortingWidget(),
            "required": False,
        })
        self.items = ()
        super(SortingFormField, self).__init__(*args, **kwargs)

    def populate(self, items):
        self.items = (SortedItem(item.pk, unicode(item)) for item in items)

    def prepare_value(self, value):
        value = clean_order_json(value)
        return iterate_in_order(self.items, value)

    def to_python(self, value):
        value = clean_order_json(value)
        return json.dumps(value)
