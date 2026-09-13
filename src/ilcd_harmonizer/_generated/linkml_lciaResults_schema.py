# Generated from linkml_lciaResults_schema.yaml by LinkML PythonGenerator.
# Regenerate with: ilcd-harmonizer generate-linkml
# id: https://example.org/ILCDlciaResults
# description:
# license: CC-BY-4.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from . linkml_shared_definitions import GlobalReferenceType, GlobalReferenceTypeId, OtherContent, OtherContentId
from linkml_runtime.linkml_model.types import Float, String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ILCDLCIA = CurieNamespace('ILCDlcia', 'https://example.org/ILCDlciaResults/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = ILCDLCIA


# Types

# Class references
class LCIAResultsId(extended_str):
    pass


class LCIAResultEntryId(extended_str):
    pass


@dataclass(repr=False)
class LCIAResults(YAMLRoot):
    """
    Top-level container for the LCIAResults section.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDLCIA["LCIAResults"]
    class_class_curie: ClassVar[str] = "ILCDlcia:LCIAResults"
    class_name: ClassVar[str] = "LCIAResults"
    class_model_uri: ClassVar[URIRef] = ILCDLCIA.LCIAResults

    id: Union[str, LCIAResultsId] = None
    LCIAResult: Optional[Union[Dict[Union[str, LCIAResultEntryId], Union[dict, "LCIAResultEntry"]], List[Union[dict, "LCIAResultEntry"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LCIAResultsId):
            self.id = LCIAResultsId(self.id)

        self._normalize_inlined_as_list(slot_name="LCIAResult", slot_type=LCIAResultEntry, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LCIAResultEntry(YAMLRoot):
    """
    Represents a single LCIA result object.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDLCIA["LCIAResultEntry"]
    class_class_curie: ClassVar[str] = "ILCDlcia:LCIAResultEntry"
    class_name: ClassVar[str] = "LCIAResultEntry"
    class_model_uri: ClassVar[URIRef] = ILCDLCIA.LCIAResultEntry

    id: Union[str, LCIAResultEntryId] = None
    referenceToLCIAMethodDataSet: Optional[Union[dict, GlobalReferenceType]] = None
    meanAmount: Optional[float] = None
    uncertaintyDistributionType: Optional[str] = None
    otherLCIA: Optional[Union[dict, OtherContent]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LCIAResultEntryId):
            self.id = LCIAResultEntryId(self.id)

        if self.referenceToLCIAMethodDataSet is not None and not isinstance(self.referenceToLCIAMethodDataSet, GlobalReferenceType):
            self.referenceToLCIAMethodDataSet = GlobalReferenceType(**as_dict(self.referenceToLCIAMethodDataSet))

        if self.meanAmount is not None and not isinstance(self.meanAmount, float):
            self.meanAmount = float(self.meanAmount)

        if self.uncertaintyDistributionType is not None and not isinstance(self.uncertaintyDistributionType, str):
            self.uncertaintyDistributionType = str(self.uncertaintyDistributionType)

        if self.otherLCIA is not None and not isinstance(self.otherLCIA, OtherContent):
            self.otherLCIA = OtherContent(**as_dict(self.otherLCIA))

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.LCIAResult = Slot(uri=ILCDLCIA.LCIAResult, name="LCIAResult", curie=ILCDLCIA.curie('LCIAResult'),
                   model_uri=ILCDLCIA.LCIAResult, domain=None, range=Optional[Union[Dict[Union[str, LCIAResultEntryId], Union[dict, LCIAResultEntry]], List[Union[dict, LCIAResultEntry]]]])

slots.referenceToLCIAMethodDataSet = Slot(uri=ILCDLCIA.referenceToLCIAMethodDataSet, name="referenceToLCIAMethodDataSet", curie=ILCDLCIA.curie('referenceToLCIAMethodDataSet'),
                   model_uri=ILCDLCIA.referenceToLCIAMethodDataSet, domain=None, range=Optional[Union[dict, GlobalReferenceType]])

slots.otherLCIA = Slot(uri=ILCDLCIA.otherLCIA, name="otherLCIA", curie=ILCDLCIA.curie('otherLCIA'),
                   model_uri=ILCDLCIA.otherLCIA, domain=None, range=Optional[Union[dict, OtherContent]])
