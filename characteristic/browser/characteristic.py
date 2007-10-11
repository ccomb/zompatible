from zope.formlib.form import EditForm, Fields

from zompatible.characteristic.interfaces import ICharacteristic, IPhysInterface

class CharacteristicEditForm(EditForm):
    def __init__(self, context, request):
        self.context, self.request = context, request
        self.label = ICharacteristic(self.context).Name()
  

class PhysInterfaceEditForm(EditForm):
    u""" Allows a product edition.
    """
    form_fields = Fields(IPhysInterface)       

        
