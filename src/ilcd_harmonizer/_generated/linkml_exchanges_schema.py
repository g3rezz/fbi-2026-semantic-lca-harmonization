# Generated from linkml_exchanges_schema.yaml by LinkML PythonGenerator.
# Regenerate with: ilcd-harmonizer generate-linkml
# id: https://example.org/ILCDexchanges
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

from . linkml_shared_definitions import GlobalReferenceType, GlobalReferenceTypeId, MultiLangString, MultiLangStringId, OtherContent, OtherContentId, UUIDType
from linkml_runtime.linkml_model.types import Boolean, Float, Integer, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ILCDEX = CurieNamespace('ILCDex', 'https://example.org/ILCDexchanges/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = ILCDEX


# Types

# Class references
class ExchangesId(extended_str):
    pass


class ExchangeEntryId(extended_str):
    pass


class FlowPropertyEntryId(extended_str):
    pass


class ExchangeClassificationId(extended_str):
    pass


class MaterialPropEntryId(extended_str):
    pass


@dataclass(repr=False)
class Exchanges(YAMLRoot):
    """
    Top-level container for the 'exchanges' section.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDEX["Exchanges"]
    class_class_curie: ClassVar[str] = "ILCDex:Exchanges"
    class_name: ClassVar[str] = "Exchanges"
    class_model_uri: ClassVar[URIRef] = ILCDEX.Exchanges

    id: Union[str, ExchangesId] = None
    exchange: Optional[Union[Dict[Union[str, ExchangeEntryId], Union[dict, "ExchangeEntry"]], List[Union[dict, "ExchangeEntry"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExchangesId):
            self.id = ExchangesId(self.id)

        self._normalize_inlined_as_list(slot_name="exchange", slot_type=ExchangeEntry, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExchangeEntry(YAMLRoot):
    """
    A single exchange entry.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDEX["ExchangeEntry"]
    class_class_curie: ClassVar[str] = "ILCDex:ExchangeEntry"
    class_name: ClassVar[str] = "ExchangeEntry"
    class_model_uri: ClassVar[URIRef] = ILCDEX.ExchangeEntry

    id: Union[str, ExchangeEntryId] = None
    dataSetInternalID: Optional[int] = None
    referenceToFlowDataSet: Optional[Union[dict, GlobalReferenceType]] = None
    meanAmount: Optional[float] = None
    referencesToDataSource: Optional[Union[dict, GlobalReferenceType]] = None
    resultingAmount: Optional[float] = None
    minimumAmount: Optional[float] = None
    maximumAmount: Optional[float] = None
    uncertaintyDistributionType: Optional[str] = None
    relativeStandardDeviation95In: Optional[str] = None
    dataSourceType: Optional[str] = None
    dataDerivationTypeStatus: Optional[str] = None
    referenceFlow: Optional[Union[bool, Bool]] = None
    resultingflowAmount: Optional[float] = None
    flowProperties: Optional[Union[Dict[Union[str, FlowPropertyEntryId], Union[dict, "FlowPropertyEntry"]], List[Union[dict, "FlowPropertyEntry"]]]] = empty_dict()
    resolvedFlowVersion: Optional[str] = None
    materialProperties: Optional[Union[Dict[Union[str, MaterialPropEntryId], Union[dict, "MaterialPropEntry"]], List[Union[dict, "MaterialPropEntry"]]]] = empty_dict()
    typeOfFlow: Optional[str] = None
    exchangeDirection: Optional[str] = None
    otherEx: Optional[Union[dict, OtherContent]] = None
    classificationEx: Optional[Union[dict, "ExchangeClassification"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExchangeEntryId):
            self.id = ExchangeEntryId(self.id)

        if self.dataSetInternalID is not None and not isinstance(self.dataSetInternalID, int):
            self.dataSetInternalID = int(self.dataSetInternalID)

        if self.referenceToFlowDataSet is not None and not isinstance(self.referenceToFlowDataSet, GlobalReferenceType):
            self.referenceToFlowDataSet = GlobalReferenceType(**as_dict(self.referenceToFlowDataSet))

        if self.meanAmount is not None and not isinstance(self.meanAmount, float):
            self.meanAmount = float(self.meanAmount)

        if self.referencesToDataSource is not None and not isinstance(self.referencesToDataSource, GlobalReferenceType):
            self.referencesToDataSource = GlobalReferenceType(**as_dict(self.referencesToDataSource))

        if self.resultingAmount is not None and not isinstance(self.resultingAmount, float):
            self.resultingAmount = float(self.resultingAmount)

        if self.minimumAmount is not None and not isinstance(self.minimumAmount, float):
            self.minimumAmount = float(self.minimumAmount)

        if self.maximumAmount is not None and not isinstance(self.maximumAmount, float):
            self.maximumAmount = float(self.maximumAmount)

        if self.uncertaintyDistributionType is not None and not isinstance(self.uncertaintyDistributionType, str):
            self.uncertaintyDistributionType = str(self.uncertaintyDistributionType)

        if self.relativeStandardDeviation95In is not None and not isinstance(self.relativeStandardDeviation95In, str):
            self.relativeStandardDeviation95In = str(self.relativeStandardDeviation95In)

        if self.dataSourceType is not None and not isinstance(self.dataSourceType, str):
            self.dataSourceType = str(self.dataSourceType)

        if self.dataDerivationTypeStatus is not None and not isinstance(self.dataDerivationTypeStatus, str):
            self.dataDerivationTypeStatus = str(self.dataDerivationTypeStatus)

        if self.referenceFlow is not None and not isinstance(self.referenceFlow, Bool):
            self.referenceFlow = Bool(self.referenceFlow)

        if self.resultingflowAmount is not None and not isinstance(self.resultingflowAmount, float):
            self.resultingflowAmount = float(self.resultingflowAmount)

        self._normalize_inlined_as_list(slot_name="flowProperties", slot_type=FlowPropertyEntry, key_name="id", keyed=True)

        if self.resolvedFlowVersion is not None and not isinstance(self.resolvedFlowVersion, str):
            self.resolvedFlowVersion = str(self.resolvedFlowVersion)

        self._normalize_inlined_as_list(slot_name="materialProperties", slot_type=MaterialPropEntry, key_name="id", keyed=True)

        if self.typeOfFlow is not None and not isinstance(self.typeOfFlow, str):
            self.typeOfFlow = str(self.typeOfFlow)

        if self.exchangeDirection is not None and not isinstance(self.exchangeDirection, str):
            self.exchangeDirection = str(self.exchangeDirection)

        if self.otherEx is not None and not isinstance(self.otherEx, OtherContent):
            self.otherEx = OtherContent(**as_dict(self.otherEx))

        if self.classificationEx is not None and not isinstance(self.classificationEx, ExchangeClassification):
            self.classificationEx = ExchangeClassification(**as_dict(self.classificationEx))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FlowPropertyEntry(YAMLRoot):
    """
    One flow property.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDEX["FlowPropertyEntry"]
    class_class_curie: ClassVar[str] = "ILCDex:FlowPropertyEntry"
    class_name: ClassVar[str] = "FlowPropertyEntry"
    class_model_uri: ClassVar[URIRef] = ILCDEX.FlowPropertyEntry

    id: Union[str, FlowPropertyEntryId] = None
    nameFP: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()
    uuidFP: Optional[str] = None
    referenceFlowProperty: Optional[Union[bool, Bool]] = None
    meanValue: Optional[float] = None
    referenceUnit: Optional[str] = None
    unitGroupUUID: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FlowPropertyEntryId):
            self.id = FlowPropertyEntryId(self.id)

        self._normalize_inlined_as_list(slot_name="nameFP", slot_type=MultiLangString, key_name="id", keyed=True)

        if self.uuidFP is not None and not isinstance(self.uuidFP, str):
            self.uuidFP = str(self.uuidFP)

        if self.referenceFlowProperty is not None and not isinstance(self.referenceFlowProperty, Bool):
            self.referenceFlowProperty = Bool(self.referenceFlowProperty)

        if self.meanValue is not None and not isinstance(self.meanValue, float):
            self.meanValue = float(self.meanValue)

        if self.referenceUnit is not None and not isinstance(self.referenceUnit, str):
            self.referenceUnit = str(self.referenceUnit)

        if self.unitGroupUUID is not None and not isinstance(self.unitGroupUUID, str):
            self.unitGroupUUID = str(self.unitGroupUUID)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExchangeClassification(YAMLRoot):
    """
    Simple object for classification with 'classHierarchy' and 'name'.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDEX["ExchangeClassification"]
    class_class_curie: ClassVar[str] = "ILCDex:ExchangeClassification"
    class_name: ClassVar[str] = "ExchangeClassification"
    class_model_uri: ClassVar[URIRef] = ILCDEX.ExchangeClassification

    id: Union[str, ExchangeClassificationId] = None
    classHierarchy: Optional[str] = None
    nameClass: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExchangeClassificationId):
            self.id = ExchangeClassificationId(self.id)

        if self.classHierarchy is not None and not isinstance(self.classHierarchy, str):
            self.classHierarchy = str(self.classHierarchy)

        if self.nameClass is not None and not isinstance(self.nameClass, str):
            self.nameClass = str(self.nameClass)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MaterialPropEntry(YAMLRoot):
    """
    Material property list with name, value, unit, unitDescription.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDEX["MaterialPropEntry"]
    class_class_curie: ClassVar[str] = "ILCDex:MaterialPropEntry"
    class_name: ClassVar[str] = "MaterialPropEntry"
    class_model_uri: ClassVar[URIRef] = ILCDEX.MaterialPropEntry

    id: Union[str, MaterialPropEntryId] = None
    name: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    unitDescription: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MaterialPropEntryId):
            self.id = MaterialPropEntryId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.unit is not None and not isinstance(self.unit, str):
            self.unit = str(self.unit)

        if self.unitDescription is not None and not isinstance(self.unitDescription, str):
            self.unitDescription = str(self.unitDescription)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.exchange = Slot(uri=ILCDEX.exchange, name="exchange", curie=ILCDEX.curie('exchange'),
                   model_uri=ILCDEX.exchange, domain=None, range=Optional[Union[Dict[Union[str, ExchangeEntryId], Union[dict, ExchangeEntry]], List[Union[dict, ExchangeEntry]]]])

slots.dataSetInternalID = Slot(uri=ILCDEX.dataSetInternalID, name="dataSetInternalID", curie=ILCDEX.curie('dataSetInternalID'),
                   model_uri=ILCDEX.dataSetInternalID, domain=None, range=Optional[int])

slots.referenceToFlowDataSet = Slot(uri=ILCDEX.referenceToFlowDataSet, name="referenceToFlowDataSet", curie=ILCDEX.curie('referenceToFlowDataSet'),
                   model_uri=ILCDEX.referenceToFlowDataSet, domain=None, range=Optional[Union[dict, GlobalReferenceType]])

slots.referenceFlow = Slot(uri=ILCDEX.referenceFlow, name="referenceFlow", curie=ILCDEX.curie('referenceFlow'),
                   model_uri=ILCDEX.referenceFlow, domain=None, range=Optional[Union[bool, Bool]])

slots.referencesToDataSource = Slot(uri=ILCDEX.referencesToDataSource, name="referencesToDataSource", curie=ILCDEX.curie('referencesToDataSource'),
                   model_uri=ILCDEX.referencesToDataSource, domain=None, range=Optional[Union[dict, GlobalReferenceType]])

slots.resultingAmount = Slot(uri=ILCDEX.resultingAmount, name="resultingAmount", curie=ILCDEX.curie('resultingAmount'),
                   model_uri=ILCDEX.resultingAmount, domain=None, range=Optional[float])

slots.minimumAmount = Slot(uri=ILCDEX.minimumAmount, name="minimumAmount", curie=ILCDEX.curie('minimumAmount'),
                   model_uri=ILCDEX.minimumAmount, domain=None, range=Optional[float])

slots.maximumAmount = Slot(uri=ILCDEX.maximumAmount, name="maximumAmount", curie=ILCDEX.curie('maximumAmount'),
                   model_uri=ILCDEX.maximumAmount, domain=None, range=Optional[float])

slots.relativeStandardDeviation95In = Slot(uri=ILCDEX.relativeStandardDeviation95In, name="relativeStandardDeviation95In", curie=ILCDEX.curie('relativeStandardDeviation95In'),
                   model_uri=ILCDEX.relativeStandardDeviation95In, domain=None, range=Optional[str])

slots.dataSourceType = Slot(uri=ILCDEX.dataSourceType, name="dataSourceType", curie=ILCDEX.curie('dataSourceType'),
                   model_uri=ILCDEX.dataSourceType, domain=None, range=Optional[str])

slots.dataDerivationTypeStatus = Slot(uri=ILCDEX.dataDerivationTypeStatus, name="dataDerivationTypeStatus", curie=ILCDEX.curie('dataDerivationTypeStatus'),
                   model_uri=ILCDEX.dataDerivationTypeStatus, domain=None, range=Optional[str])

slots.resultingflowAmount = Slot(uri=ILCDEX.resultingflowAmount, name="resultingflowAmount", curie=ILCDEX.curie('resultingflowAmount'),
                   model_uri=ILCDEX.resultingflowAmount, domain=None, range=Optional[float])

slots.flowProperties = Slot(uri=ILCDEX.flowProperties, name="flowProperties", curie=ILCDEX.curie('flowProperties'),
                   model_uri=ILCDEX.flowProperties, domain=None, range=Optional[Union[Dict[Union[str, FlowPropertyEntryId], Union[dict, FlowPropertyEntry]], List[Union[dict, FlowPropertyEntry]]]])

slots.materialProperties = Slot(uri=ILCDEX.materialProperties, name="materialProperties", curie=ILCDEX.curie('materialProperties'),
                   model_uri=ILCDEX.materialProperties, domain=None, range=Optional[Union[Dict[Union[str, MaterialPropEntryId], Union[dict, MaterialPropEntry]], List[Union[dict, MaterialPropEntry]]]])

slots.resolvedFlowVersion = Slot(uri=ILCDEX.resolvedFlowVersion, name="resolvedFlowVersion", curie=ILCDEX.curie('resolvedFlowVersion'),
                   model_uri=ILCDEX.resolvedFlowVersion, domain=None, range=Optional[str])

slots.typeOfFlow = Slot(uri=ILCDEX.typeOfFlow, name="typeOfFlow", curie=ILCDEX.curie('typeOfFlow'),
                   model_uri=ILCDEX.typeOfFlow, domain=None, range=Optional[str])

slots.exchangeDirection = Slot(uri=ILCDEX.exchangeDirection, name="exchangeDirection", curie=ILCDEX.curie('exchangeDirection'),
                   model_uri=ILCDEX.exchangeDirection, domain=None, range=Optional[str])

slots.otherEx = Slot(uri=ILCDEX.otherEx, name="otherEx", curie=ILCDEX.curie('otherEx'),
                   model_uri=ILCDEX.otherEx, domain=None, range=Optional[Union[dict, OtherContent]])

slots.classificationEx = Slot(uri=ILCDEX.classificationEx, name="classificationEx", curie=ILCDEX.curie('classificationEx'),
                   model_uri=ILCDEX.classificationEx, domain=None, range=Optional[Union[dict, ExchangeClassification]])

slots.uuidFP = Slot(uri=ILCDEX.uuidFP, name="uuidFP", curie=ILCDEX.curie('uuidFP'),
                   model_uri=ILCDEX.uuidFP, domain=None, range=Optional[str])

slots.referenceFlowProperty = Slot(uri=ILCDEX.referenceFlowProperty, name="referenceFlowProperty", curie=ILCDEX.curie('referenceFlowProperty'),
                   model_uri=ILCDEX.referenceFlowProperty, domain=None, range=Optional[Union[bool, Bool]])

slots.meanValue = Slot(uri=ILCDEX.meanValue, name="meanValue", curie=ILCDEX.curie('meanValue'),
                   model_uri=ILCDEX.meanValue, domain=None, range=Optional[float])

slots.referenceUnit = Slot(uri=ILCDEX.referenceUnit, name="referenceUnit", curie=ILCDEX.curie('referenceUnit'),
                   model_uri=ILCDEX.referenceUnit, domain=None, range=Optional[str])

slots.unitGroupUUID = Slot(uri=ILCDEX.unitGroupUUID, name="unitGroupUUID", curie=ILCDEX.curie('unitGroupUUID'),
                   model_uri=ILCDEX.unitGroupUUID, domain=None, range=Optional[str])

slots.classHierarchy = Slot(uri=ILCDEX.classHierarchy, name="classHierarchy", curie=ILCDEX.curie('classHierarchy'),
                   model_uri=ILCDEX.classHierarchy, domain=None, range=Optional[str])

slots.nameClass = Slot(uri=ILCDEX.nameClass, name="nameClass", curie=ILCDEX.curie('nameClass'),
                   model_uri=ILCDEX.nameClass, domain=None, range=Optional[str])

slots.nameFP = Slot(uri=ILCDEX.nameFP, name="nameFP", curie=ILCDEX.curie('nameFP'),
                   model_uri=ILCDEX.nameFP, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.unit = Slot(uri=ILCDEX.unit, name="unit", curie=ILCDEX.curie('unit'),
                   model_uri=ILCDEX.unit, domain=None, range=Optional[str])

slots.unitDescription = Slot(uri=ILCDEX.unitDescription, name="unitDescription", curie=ILCDEX.curie('unitDescription'),
                   model_uri=ILCDEX.unitDescription, domain=None, range=Optional[str])
