from zope.formlib.form import EditForm, Fields

from zompatible.characteristic.interfaces import ICharacteristicManager, \
                                                 ICharacteristic, \
                                                 IPhysInterface,  \
                                                 IResolution, \
                                                 IFlashCardSlots

class CharacteristicEditForm(EditForm):
    
    def __init__(self, context, request):
        self.context, self.request = context, request
        self.label = ICharacteristic(self.context).Name()

  
class CharacterizableEditForm(EditForm):
    u""" Edit the characteristic list.
    """
    form_fields = Fields(ICharacteristicManager) 

class PhysInterfaceEditForm(CharacteristicEditForm):
    u""" Allows a characteristic edition.
    """
    form_fields = Fields(IPhysInterface) 

class ResolutionEditForm(CharacteristicEditForm):
    u""" Allows a characteristic edition.
    """
    form_fields = Fields(IResolution)       

class FlashCardSlotsEditForm(CharacteristicEditForm):
    u""" Allows a characteristic edition.
    """
    form_fields = Fields(IFlashCardSlots)       
        
