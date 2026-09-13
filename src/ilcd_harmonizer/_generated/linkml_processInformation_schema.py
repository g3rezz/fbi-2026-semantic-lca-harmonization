# Generated from linkml_processInformation_schema.yaml by LinkML PythonGenerator.
# Regenerate with: ilcd-harmonizer generate-linkml
# id: https://example.org/ILCDprocessInformation
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

from . linkml_shared_definitions import GlobalReferenceType, GlobalReferenceTypeId, MultiLangString, MultiLangStringId, OtherContent, OtherContentId, UUIDType, Year
from linkml_runtime.linkml_model.types import Integer, String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ILCDPI = CurieNamespace('ILCDpi', 'https://example.org/ILCDprocessInformation/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = ILCDPI


# Types

# Class references
class ProcessInformationId(extended_str):
    pass


class DataSetInformationId(extended_str):
    pass


class DataSetNameId(extended_str):
    pass


class ClassificationInformationId(extended_str):
    pass


class ClassificationId(extended_str):
    pass


class ClassificationEntryId(extended_str):
    pass


class QuantitativeReferenceId(extended_str):
    pass


class TimeInformationId(extended_str):
    pass


class GeographyInformationId(extended_str):
    pass


class LocationInfoId(extended_str):
    pass


class TechnologyInformationId(extended_str):
    pass


@dataclass(repr=False)
class ProcessInformation(YAMLRoot):
    """
    Container for the process information section.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["ProcessInformation"]
    class_class_curie: ClassVar[str] = "ILCDpi:ProcessInformation"
    class_name: ClassVar[str] = "ProcessInformation"
    class_model_uri: ClassVar[URIRef] = ILCDPI.ProcessInformation

    id: Union[str, ProcessInformationId] = None
    dataSetInformation: Union[dict, "DataSetInformation"] = None
    quantitativeReference: Optional[Union[dict, "QuantitativeReference"]] = None
    timeInformation: Optional[Union[dict, "TimeInformation"]] = None
    geography: Optional[Union[dict, "GeographyInformation"]] = None
    technology: Optional[Union[dict, "TechnologyInformation"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcessInformationId):
            self.id = ProcessInformationId(self.id)

        if self._is_empty(self.dataSetInformation):
            self.MissingRequiredField("dataSetInformation")
        if not isinstance(self.dataSetInformation, DataSetInformation):
            self.dataSetInformation = DataSetInformation(**as_dict(self.dataSetInformation))

        if self.quantitativeReference is not None and not isinstance(self.quantitativeReference, QuantitativeReference):
            self.quantitativeReference = QuantitativeReference(**as_dict(self.quantitativeReference))

        if self.timeInformation is not None and not isinstance(self.timeInformation, TimeInformation):
            self.timeInformation = TimeInformation(**as_dict(self.timeInformation))

        if self.geography is not None and not isinstance(self.geography, GeographyInformation):
            self.geography = GeographyInformation(**as_dict(self.geography))

        if self.technology is not None and not isinstance(self.technology, TechnologyInformation):
            self.technology = TechnologyInformation(**as_dict(self.technology))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataSetInformation(YAMLRoot):
    """
    Data set information details.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["DataSetInformation"]
    class_class_curie: ClassVar[str] = "ILCDpi:DataSetInformation"
    class_name: ClassVar[str] = "DataSetInformation"
    class_model_uri: ClassVar[URIRef] = ILCDPI.DataSetInformation

    id: Union[str, DataSetInformationId] = None
    UUID: str = None
    dataSetName: Optional[Union[dict, "DataSetName"]] = None
    synonyms: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()
    classificationInformation: Optional[Union[dict, "ClassificationInformation"]] = None
    generalComment: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()
    referenceToExternalDocumentation: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()
    otherDSI: Optional[Union[dict, OtherContent]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataSetInformationId):
            self.id = DataSetInformationId(self.id)

        if self._is_empty(self.UUID):
            self.MissingRequiredField("UUID")
        if not isinstance(self.UUID, str):
            self.UUID = str(self.UUID)

        if self.dataSetName is not None and not isinstance(self.dataSetName, DataSetName):
            self.dataSetName = DataSetName(**as_dict(self.dataSetName))

        self._normalize_inlined_as_list(slot_name="synonyms", slot_type=MultiLangString, key_name="id", keyed=True)

        if self.classificationInformation is not None and not isinstance(self.classificationInformation, ClassificationInformation):
            self.classificationInformation = ClassificationInformation(**as_dict(self.classificationInformation))

        self._normalize_inlined_as_list(slot_name="generalComment", slot_type=MultiLangString, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="referenceToExternalDocumentation", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        if self.otherDSI is not None and not isinstance(self.otherDSI, OtherContent):
            self.otherDSI = OtherContent(**as_dict(self.otherDSI))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataSetName(YAMLRoot):
    """
    Container for the data set name.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["DataSetName"]
    class_class_curie: ClassVar[str] = "ILCDpi:DataSetName"
    class_name: ClassVar[str] = "DataSetName"
    class_model_uri: ClassVar[URIRef] = ILCDPI.DataSetName

    id: Union[str, DataSetNameId] = None
    baseName: Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]] = empty_dict()
    functionalUnitFlowProperties: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataSetNameId):
            self.id = DataSetNameId(self.id)

        if self._is_empty(self.baseName):
            self.MissingRequiredField("baseName")
        self._normalize_inlined_as_list(slot_name="baseName", slot_type=MultiLangString, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="functionalUnitFlowProperties", slot_type=MultiLangString, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ClassificationInformation(YAMLRoot):
    """
    Classification information for the data set.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["ClassificationInformation"]
    class_class_curie: ClassVar[str] = "ILCDpi:ClassificationInformation"
    class_name: ClassVar[str] = "ClassificationInformation"
    class_model_uri: ClassVar[URIRef] = ILCDPI.ClassificationInformation

    id: Union[str, ClassificationInformationId] = None
    classification: Optional[Union[Dict[Union[str, ClassificationId], Union[dict, "Classification"]], List[Union[dict, "Classification"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ClassificationInformationId):
            self.id = ClassificationInformationId(self.id)

        self._normalize_inlined_as_list(slot_name="classification", slot_type=Classification, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Classification(YAMLRoot):
    """
    Classification object.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["Classification"]
    class_class_curie: ClassVar[str] = "ILCDpi:Classification"
    class_name: ClassVar[str] = "Classification"
    class_model_uri: ClassVar[URIRef] = ILCDPI.Classification

    id: Union[str, ClassificationId] = None
    name: Optional[str] = None
    classEntries: Optional[Union[Dict[Union[str, ClassificationEntryId], Union[dict, "ClassificationEntry"]], List[Union[dict, "ClassificationEntry"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ClassificationId):
            self.id = ClassificationId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        self._normalize_inlined_as_list(slot_name="classEntries", slot_type=ClassificationEntry, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ClassificationEntry(YAMLRoot):
    """
    Classification entry.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["ClassificationEntry"]
    class_class_curie: ClassVar[str] = "ILCDpi:ClassificationEntry"
    class_name: ClassVar[str] = "ClassificationEntry"
    class_model_uri: ClassVar[URIRef] = ILCDPI.ClassificationEntry

    id: Union[str, ClassificationEntryId] = None
    value: Optional[str] = None
    level: Optional[int] = None
    classId: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ClassificationEntryId):
            self.id = ClassificationEntryId(self.id)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.level is not None and not isinstance(self.level, int):
            self.level = int(self.level)

        if self.classId is not None and not isinstance(self.classId, str):
            self.classId = str(self.classId)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QuantitativeReference(YAMLRoot):
    """
    Quantitative reference details.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["QuantitativeReference"]
    class_class_curie: ClassVar[str] = "ILCDpi:QuantitativeReference"
    class_name: ClassVar[str] = "QuantitativeReference"
    class_model_uri: ClassVar[URIRef] = ILCDPI.QuantitativeReference

    id: Union[str, QuantitativeReferenceId] = None
    referenceToReferenceFlow: Optional[Union[int, List[int]]] = empty_list()
    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, QuantitativeReferenceId):
            self.id = QuantitativeReferenceId(self.id)

        if not isinstance(self.referenceToReferenceFlow, list):
            self.referenceToReferenceFlow = [self.referenceToReferenceFlow] if self.referenceToReferenceFlow is not None else []
        self.referenceToReferenceFlow = [v if isinstance(v, int) else int(v) for v in self.referenceToReferenceFlow]

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TimeInformation(YAMLRoot):
    """
    Time-related information for the data set.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["TimeInformation"]
    class_class_curie: ClassVar[str] = "ILCDpi:TimeInformation"
    class_name: ClassVar[str] = "TimeInformation"
    class_model_uri: ClassVar[URIRef] = ILCDPI.TimeInformation

    id: Union[str, TimeInformationId] = None
    referenceYear: Optional[int] = None
    dataSetValidUntil: Optional[int] = None
    timeRepresentativenessDescription: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()
    otherTime: Optional[Union[dict, OtherContent]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TimeInformationId):
            self.id = TimeInformationId(self.id)

        if self.referenceYear is not None and not isinstance(self.referenceYear, int):
            self.referenceYear = int(self.referenceYear)

        if self.dataSetValidUntil is not None and not isinstance(self.dataSetValidUntil, int):
            self.dataSetValidUntil = int(self.dataSetValidUntil)

        self._normalize_inlined_as_list(slot_name="timeRepresentativenessDescription", slot_type=MultiLangString, key_name="id", keyed=True)

        if self.otherTime is not None and not isinstance(self.otherTime, OtherContent):
            self.otherTime = OtherContent(**as_dict(self.otherTime))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GeographyInformation(YAMLRoot):
    """
    Geographical information details.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["GeographyInformation"]
    class_class_curie: ClassVar[str] = "ILCDpi:GeographyInformation"
    class_name: ClassVar[str] = "GeographyInformation"
    class_model_uri: ClassVar[URIRef] = ILCDPI.GeographyInformation

    id: Union[str, GeographyInformationId] = None
    locationOfOperationSupplyOrProduction: Optional[Union[dict, "LocationInfo"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeographyInformationId):
            self.id = GeographyInformationId(self.id)

        if self.locationOfOperationSupplyOrProduction is not None and not isinstance(self.locationOfOperationSupplyOrProduction, LocationInfo):
            self.locationOfOperationSupplyOrProduction = LocationInfo(**as_dict(self.locationOfOperationSupplyOrProduction))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LocationInfo(YAMLRoot):
    """
    Location details.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["LocationInfo"]
    class_class_curie: ClassVar[str] = "ILCDpi:LocationInfo"
    class_name: ClassVar[str] = "LocationInfo"
    class_model_uri: ClassVar[URIRef] = ILCDPI.LocationInfo

    id: Union[str, LocationInfoId] = None
    descriptionOfRestrictions: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()
    location: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LocationInfoId):
            self.id = LocationInfoId(self.id)

        self._normalize_inlined_as_list(slot_name="descriptionOfRestrictions", slot_type=MultiLangString, key_name="id", keyed=True)

        if self.location is not None and not isinstance(self.location, str):
            self.location = str(self.location)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TechnologyInformation(YAMLRoot):
    """
    Technology information for the data set.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDPI["TechnologyInformation"]
    class_class_curie: ClassVar[str] = "ILCDpi:TechnologyInformation"
    class_name: ClassVar[str] = "TechnologyInformation"
    class_model_uri: ClassVar[URIRef] = ILCDPI.TechnologyInformation

    id: Union[str, TechnologyInformationId] = None
    technologyDescriptionAndIncludedProcesses: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()
    technologicalApplicability: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()
    referenceToTechnologyFlowDiagrammOrPicture: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()
    referenceToTechnologyPictogramme: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TechnologyInformationId):
            self.id = TechnologyInformationId(self.id)

        self._normalize_inlined_as_list(slot_name="technologyDescriptionAndIncludedProcesses", slot_type=MultiLangString, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="technologicalApplicability", slot_type=MultiLangString, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="referenceToTechnologyFlowDiagrammOrPicture", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="referenceToTechnologyPictogramme", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.dataSetInformation = Slot(uri=ILCDPI.dataSetInformation, name="dataSetInformation", curie=ILCDPI.curie('dataSetInformation'),
                   model_uri=ILCDPI.dataSetInformation, domain=None, range=Union[dict, DataSetInformation])

slots.quantitativeReference = Slot(uri=ILCDPI.quantitativeReference, name="quantitativeReference", curie=ILCDPI.curie('quantitativeReference'),
                   model_uri=ILCDPI.quantitativeReference, domain=None, range=Optional[Union[dict, QuantitativeReference]])

slots.timeInformation = Slot(uri=ILCDPI.timeInformation, name="timeInformation", curie=ILCDPI.curie('timeInformation'),
                   model_uri=ILCDPI.timeInformation, domain=None, range=Optional[Union[dict, TimeInformation]])

slots.geography = Slot(uri=ILCDPI.geography, name="geography", curie=ILCDPI.curie('geography'),
                   model_uri=ILCDPI.geography, domain=None, range=Optional[Union[dict, GeographyInformation]])

slots.technology = Slot(uri=ILCDPI.technology, name="technology", curie=ILCDPI.curie('technology'),
                   model_uri=ILCDPI.technology, domain=None, range=Optional[Union[dict, TechnologyInformation]])

slots.dataSetName = Slot(uri=ILCDPI.dataSetName, name="dataSetName", curie=ILCDPI.curie('dataSetName'),
                   model_uri=ILCDPI.dataSetName, domain=None, range=Optional[Union[dict, DataSetName]])

slots.synonyms = Slot(uri=ILCDPI.synonyms, name="synonyms", curie=ILCDPI.curie('synonyms'),
                   model_uri=ILCDPI.synonyms, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.classificationInformation = Slot(uri=ILCDPI.classificationInformation, name="classificationInformation", curie=ILCDPI.curie('classificationInformation'),
                   model_uri=ILCDPI.classificationInformation, domain=None, range=Optional[Union[dict, ClassificationInformation]])

slots.generalComment = Slot(uri=ILCDPI.generalComment, name="generalComment", curie=ILCDPI.curie('generalComment'),
                   model_uri=ILCDPI.generalComment, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.referenceToExternalDocumentation = Slot(uri=ILCDPI.referenceToExternalDocumentation, name="referenceToExternalDocumentation", curie=ILCDPI.curie('referenceToExternalDocumentation'),
                   model_uri=ILCDPI.referenceToExternalDocumentation, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.otherDSI = Slot(uri=ILCDPI.otherDSI, name="otherDSI", curie=ILCDPI.curie('otherDSI'),
                   model_uri=ILCDPI.otherDSI, domain=None, range=Optional[Union[dict, OtherContent]])

slots.baseName = Slot(uri=ILCDPI.baseName, name="baseName", curie=ILCDPI.curie('baseName'),
                   model_uri=ILCDPI.baseName, domain=None, range=Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]])

slots.functionalUnitFlowProperties = Slot(uri=ILCDPI.functionalUnitFlowProperties, name="functionalUnitFlowProperties", curie=ILCDPI.curie('functionalUnitFlowProperties'),
                   model_uri=ILCDPI.functionalUnitFlowProperties, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.classification = Slot(uri=ILCDPI.classification, name="classification", curie=ILCDPI.curie('classification'),
                   model_uri=ILCDPI.classification, domain=None, range=Optional[Union[Dict[Union[str, ClassificationId], Union[dict, Classification]], List[Union[dict, Classification]]]])

slots.classEntries = Slot(uri=ILCDPI.classEntries, name="classEntries", curie=ILCDPI.curie('classEntries'),
                   model_uri=ILCDPI.classEntries, domain=None, range=Optional[Union[Dict[Union[str, ClassificationEntryId], Union[dict, ClassificationEntry]], List[Union[dict, ClassificationEntry]]]])

slots.level = Slot(uri=ILCDPI.level, name="level", curie=ILCDPI.curie('level'),
                   model_uri=ILCDPI.level, domain=None, range=Optional[int])

slots.classId = Slot(uri=ILCDPI.classId, name="classId", curie=ILCDPI.curie('classId'),
                   model_uri=ILCDPI.classId, domain=None, range=Optional[str])

slots.referenceToReferenceFlow = Slot(uri=ILCDPI.referenceToReferenceFlow, name="referenceToReferenceFlow", curie=ILCDPI.curie('referenceToReferenceFlow'),
                   model_uri=ILCDPI.referenceToReferenceFlow, domain=None, range=Optional[Union[int, List[int]]])

slots.referenceYear = Slot(uri=ILCDPI.referenceYear, name="referenceYear", curie=ILCDPI.curie('referenceYear'),
                   model_uri=ILCDPI.referenceYear, domain=None, range=Optional[int])

slots.dataSetValidUntil = Slot(uri=ILCDPI.dataSetValidUntil, name="dataSetValidUntil", curie=ILCDPI.curie('dataSetValidUntil'),
                   model_uri=ILCDPI.dataSetValidUntil, domain=None, range=Optional[int])

slots.timeRepresentativenessDescription = Slot(uri=ILCDPI.timeRepresentativenessDescription, name="timeRepresentativenessDescription", curie=ILCDPI.curie('timeRepresentativenessDescription'),
                   model_uri=ILCDPI.timeRepresentativenessDescription, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.otherTime = Slot(uri=ILCDPI.otherTime, name="otherTime", curie=ILCDPI.curie('otherTime'),
                   model_uri=ILCDPI.otherTime, domain=None, range=Optional[Union[dict, OtherContent]])

slots.locationOfOperationSupplyOrProduction = Slot(uri=ILCDPI.locationOfOperationSupplyOrProduction, name="locationOfOperationSupplyOrProduction", curie=ILCDPI.curie('locationOfOperationSupplyOrProduction'),
                   model_uri=ILCDPI.locationOfOperationSupplyOrProduction, domain=None, range=Optional[Union[dict, LocationInfo]])

slots.descriptionOfRestrictions = Slot(uri=ILCDPI.descriptionOfRestrictions, name="descriptionOfRestrictions", curie=ILCDPI.curie('descriptionOfRestrictions'),
                   model_uri=ILCDPI.descriptionOfRestrictions, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.location = Slot(uri=ILCDPI.location, name="location", curie=ILCDPI.curie('location'),
                   model_uri=ILCDPI.location, domain=None, range=Optional[str])

slots.technologyDescriptionAndIncludedProcesses = Slot(uri=ILCDPI.technologyDescriptionAndIncludedProcesses, name="technologyDescriptionAndIncludedProcesses", curie=ILCDPI.curie('technologyDescriptionAndIncludedProcesses'),
                   model_uri=ILCDPI.technologyDescriptionAndIncludedProcesses, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.technologicalApplicability = Slot(uri=ILCDPI.technologicalApplicability, name="technologicalApplicability", curie=ILCDPI.curie('technologicalApplicability'),
                   model_uri=ILCDPI.technologicalApplicability, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.referenceToTechnologyFlowDiagrammOrPicture = Slot(uri=ILCDPI.referenceToTechnologyFlowDiagrammOrPicture, name="referenceToTechnologyFlowDiagrammOrPicture", curie=ILCDPI.curie('referenceToTechnologyFlowDiagrammOrPicture'),
                   model_uri=ILCDPI.referenceToTechnologyFlowDiagrammOrPicture, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.referenceToTechnologyPictogramme = Slot(uri=ILCDPI.referenceToTechnologyPictogramme, name="referenceToTechnologyPictogramme", curie=ILCDPI.curie('referenceToTechnologyPictogramme'),
                   model_uri=ILCDPI.referenceToTechnologyPictogramme, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])
