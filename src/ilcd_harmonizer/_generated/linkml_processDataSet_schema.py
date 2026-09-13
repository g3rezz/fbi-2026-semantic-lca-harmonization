# Generated from linkml_processDataSet_schema.yaml by LinkML PythonGenerator.
# Regenerate with: ilcd-harmonizer generate-linkml
# id: https://example.org/ilcd
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

from . linkml_administrativeInformation_schema import AdministrativeInformation, AdministrativeInformationId
from . linkml_exchanges_schema import Exchanges, ExchangesId
from . linkml_lciaResults_schema import LCIAResults, LCIAResultsId
from . linkml_modellingAndValidation_schema import ModellingAndValidation, ModellingAndValidationId
from . linkml_processInformation_schema import ProcessInformation, ProcessInformationId
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ILCD = CurieNamespace('ilcd', 'https://example.org/ilcd/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = ILCD


# Types

# Class references
class ProcessDataSetId(extended_str):
    pass


@dataclass(repr=False)
class ProcessDataSet(YAMLRoot):
    """
    Root of the unified ILCD schema
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCD["ProcessDataSet"]
    class_class_curie: ClassVar[str] = "ilcd:ProcessDataSet"
    class_name: ClassVar[str] = "ProcessDataSet"
    class_model_uri: ClassVar[URIRef] = ILCD.ProcessDataSet

    id: Union[str, ProcessDataSetId] = None
    processInformation: Union[dict, ProcessInformation] = None
    modellingAndValidation: Optional[Union[dict, ModellingAndValidation]] = None
    administrativeInformation: Optional[Union[dict, AdministrativeInformation]] = None
    exchanges: Optional[Union[dict, Exchanges]] = None
    lciaResults: Optional[Union[dict, LCIAResults]] = None
    version: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcessDataSetId):
            self.id = ProcessDataSetId(self.id)

        if self._is_empty(self.processInformation):
            self.MissingRequiredField("processInformation")
        if not isinstance(self.processInformation, ProcessInformation):
            self.processInformation = ProcessInformation(**as_dict(self.processInformation))

        if self.modellingAndValidation is not None and not isinstance(self.modellingAndValidation, ModellingAndValidation):
            self.modellingAndValidation = ModellingAndValidation(**as_dict(self.modellingAndValidation))

        if self.administrativeInformation is not None and not isinstance(self.administrativeInformation, AdministrativeInformation):
            self.administrativeInformation = AdministrativeInformation(**as_dict(self.administrativeInformation))

        if self.exchanges is not None and not isinstance(self.exchanges, Exchanges):
            self.exchanges = Exchanges(**as_dict(self.exchanges))

        if self.lciaResults is not None and not isinstance(self.lciaResults, LCIAResults):
            self.lciaResults = LCIAResults(**as_dict(self.lciaResults))

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.processInformation = Slot(uri=ILCD.processInformation, name="processInformation", curie=ILCD.curie('processInformation'),
                   model_uri=ILCD.processInformation, domain=None, range=str)

slots.modellingAndValidation = Slot(uri=ILCD.modellingAndValidation, name="modellingAndValidation", curie=ILCD.curie('modellingAndValidation'),
                   model_uri=ILCD.modellingAndValidation, domain=None, range=Optional[str])

slots.administrativeInformation = Slot(uri=ILCD.administrativeInformation, name="administrativeInformation", curie=ILCD.curie('administrativeInformation'),
                   model_uri=ILCD.administrativeInformation, domain=None, range=Optional[str])

slots.exchanges = Slot(uri=ILCD.exchanges, name="exchanges", curie=ILCD.curie('exchanges'),
                   model_uri=ILCD.exchanges, domain=None, range=Optional[str])

slots.lciaResults = Slot(uri=ILCD.lciaResults, name="lciaResults", curie=ILCD.curie('lciaResults'),
                   model_uri=ILCD.lciaResults, domain=None, range=Optional[str])

slots.ProcessDataSet_processInformation = Slot(uri=ILCD.processInformation, name="ProcessDataSet_processInformation", curie=ILCD.curie('processInformation'),
                   model_uri=ILCD.ProcessDataSet_processInformation, domain=ProcessDataSet, range=Union[dict, ProcessInformation])

slots.ProcessDataSet_modellingAndValidation = Slot(uri=ILCD.modellingAndValidation, name="ProcessDataSet_modellingAndValidation", curie=ILCD.curie('modellingAndValidation'),
                   model_uri=ILCD.ProcessDataSet_modellingAndValidation, domain=ProcessDataSet, range=Optional[Union[dict, ModellingAndValidation]])

slots.ProcessDataSet_administrativeInformation = Slot(uri=ILCD.administrativeInformation, name="ProcessDataSet_administrativeInformation", curie=ILCD.curie('administrativeInformation'),
                   model_uri=ILCD.ProcessDataSet_administrativeInformation, domain=ProcessDataSet, range=Optional[Union[dict, AdministrativeInformation]])

slots.ProcessDataSet_exchanges = Slot(uri=ILCD.exchanges, name="ProcessDataSet_exchanges", curie=ILCD.curie('exchanges'),
                   model_uri=ILCD.ProcessDataSet_exchanges, domain=ProcessDataSet, range=Optional[Union[dict, Exchanges]])

slots.ProcessDataSet_lciaResults = Slot(uri=ILCD.lciaResults, name="ProcessDataSet_lciaResults", curie=ILCD.curie('lciaResults'),
                   model_uri=ILCD.ProcessDataSet_lciaResults, domain=ProcessDataSet, range=Optional[Union[dict, LCIAResults]])
