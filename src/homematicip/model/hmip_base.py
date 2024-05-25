from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr


class HmipBaseModel(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True
    )

    _on_remove_handler: list = PrivateAttr(default_factory=list)
    _on_update_handler: list = PrivateAttr(default_factory=list)

    def fire_on_remove(self):
        """Call all subscribers of the on_remove event."""
        for subscriber in self._on_remove_handler:
            subscriber(self)

    def fire_on_update(self):
        """Call all subscribers of the on_update event."""
        for subscriber in self._on_update_handler:
            subscriber(self)

    def subscribe_on_remove(self, subscriber):
        """Subscribe to the on_remove event of this model. The subscriber will be called with the removed model as
        argument."""
        if subscriber not in self._on_remove_handler:
            self._on_remove_handler.append(subscriber)

    def unsubscribe_on_remove(self, subscriber):
        """Unsubscribe from the on_remove event of this model."""
        if subscriber in self._on_remove_handler:
            self._on_remove_handler.remove(subscriber)

    def subscribe_on_update(self, subscriber):
        """Subscribe to the on_update event of this model. The subscriber will be called with the updated model as
        argument."""
        if subscriber not in self._on_update_handler:
            self._on_update_handler.append(subscriber)

    def unsubscribe_on_update(self, subscriber):
        """Unsubscribe from the on_update event of this model."""
        if subscriber in self._on_update_handler:
            self._on_update_handler.remove(subscriber)

    def update_from_dict(self, data_dict):
        """Update this model from a dictionary. This will call all subscribers of the on_update event."""

        model_fields = self.model_fields
        new_item = type(self).model_validate(data_dict, strict=False)

        for field_name in model_fields.keys():

            if hasattr(new_item, field_name):
                new_value = getattr(new_item, field_name)
            else:
                new_value = None

            setattr(self, field_name, new_value)

        # raise on update event and notify all subscribers
        self.fire_on_update()

    def remove_object(self):
        """Must be called, when this item has been removed from the object tree. This will call all subscribers of the
        on_remove event."""
        self.fire_on_remove()
