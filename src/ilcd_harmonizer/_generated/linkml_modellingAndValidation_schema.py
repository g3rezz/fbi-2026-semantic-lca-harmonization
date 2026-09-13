# Generated from linkml_modellingAndValidation_schema.yaml by LinkML PythonGenerator.
# Regenerate with: ilcd-harmonizer generate-linkml
# id: https://example.org/ILCDmodellingAndValidation
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

from . linkml_shared_definitions import GlobalReferenceType, GlobalReferenceTypeId, MultiLangString, MultiLangStringId, OtherContent, OtherContentId, ResourceURL, UUIDType
from linkml_runtime.linkml_model.types import Boolean, Integer, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ILCDMAV = CurieNamespace('ILCDmav', 'https://example.org/ILCDmodellingAndValidation/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = ILCDMAV


# Types

# Class references
class ModellingAndValidationId(extended_str):
    pass


class LCIMethodAndAllocationEntryId(extended_str):
    pass


class DataSourcesTreatmentAndRepresentativenessId(extended_str):
    pass


class ValidationInfoId(extended_str):
    pass


class ReviewEntryId(extended_str):
    pass


class ComplianceDeclarationsId(extended_str):
    pass


class ComplianceEntryId(extended_str):
    pass


class DSTAROtherRootId(extended_str):
    pass


class DSTAREntryId(extended_str):
    pass


class DSTARReferenceId(extended_str):
    pass


class ExtendedMultiLangStringId(extended_str):
    pass


class VersionDictId(extended_str):
    pass


class UUIDDictId(extended_str):
    pass


@dataclass(repr=False)
class ModellingAndValidation(YAMLRoot):
    """
    Top-level container for the modellingAndValidation section.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ModellingAndValidation"]
    class_class_curie: ClassVar[str] = "ILCDmav:ModellingAndValidation"
    class_name: ClassVar[str] = "ModellingAndValidation"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ModellingAndValidation

    id: Union[str, ModellingAndValidationId] = None
    LCIMethodAndAllocation: Optional[Union[dict, "LCIMethodAndAllocationEntry"]] = None
    dataSourcesTreatmentAndRepresentativeness: Optional[Union[dict, "DataSourcesTreatmentAndRepresentativeness"]] = None
    validationInfo: Optional[Union[dict, "ValidationInfo"]] = None
    complianceDeclarations: Optional[Union[dict, "ComplianceDeclarations"]] = None
    otherMAV: Optional[Union[dict, OtherContent]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ModellingAndValidationId):
            self.id = ModellingAndValidationId(self.id)

        if self.LCIMethodAndAllocation is not None and not isinstance(self.LCIMethodAndAllocation, LCIMethodAndAllocationEntry):
            self.LCIMethodAndAllocation = LCIMethodAndAllocationEntry(**as_dict(self.LCIMethodAndAllocation))

        if self.dataSourcesTreatmentAndRepresentativeness is not None and not isinstance(self.dataSourcesTreatmentAndRepresentativeness, DataSourcesTreatmentAndRepresentativeness):
            self.dataSourcesTreatmentAndRepresentativeness = DataSourcesTreatmentAndRepresentativeness(**as_dict(self.dataSourcesTreatmentAndRepresentativeness))

        if self.validationInfo is not None and not isinstance(self.validationInfo, ValidationInfo):
            self.validationInfo = ValidationInfo(**as_dict(self.validationInfo))

        if self.complianceDeclarations is not None and not isinstance(self.complianceDeclarations, ComplianceDeclarations):
            self.complianceDeclarations = ComplianceDeclarations(**as_dict(self.complianceDeclarations))

        if self.otherMAV is not None and not isinstance(self.otherMAV, OtherContent):
            self.otherMAV = OtherContent(**as_dict(self.otherMAV))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LCIMethodAndAllocationEntry(YAMLRoot):
    """
    Holds LCI method, allocation info, references, and other content.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["LCIMethodAndAllocationEntry"]
    class_class_curie: ClassVar[str] = "ILCDmav:LCIMethodAndAllocationEntry"
    class_name: ClassVar[str] = "LCIMethodAndAllocationEntry"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.LCIMethodAndAllocationEntry

    id: Union[str, LCIMethodAndAllocationEntryId] = None
    typeOfDataSet: Optional[str] = None
    referenceToLCAMethodDetails: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()
    otherMAA: Optional[Union[dict, OtherContent]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LCIMethodAndAllocationEntryId):
            self.id = LCIMethodAndAllocationEntryId(self.id)

        if self.typeOfDataSet is not None and not isinstance(self.typeOfDataSet, str):
            self.typeOfDataSet = str(self.typeOfDataSet)

        self._normalize_inlined_as_list(slot_name="referenceToLCAMethodDetails", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        if self.otherMAA is not None and not isinstance(self.otherMAA, OtherContent):
            self.otherMAA = OtherContent(**as_dict(self.otherMAA))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataSourcesTreatmentAndRepresentativeness(YAMLRoot):
    """
    Holds references to data sources, usage advice, and other extras.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["DataSourcesTreatmentAndRepresentativeness"]
    class_class_curie: ClassVar[str] = "ILCDmav:DataSourcesTreatmentAndRepresentativeness"
    class_name: ClassVar[str] = "DataSourcesTreatmentAndRepresentativeness"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.DataSourcesTreatmentAndRepresentativeness

    id: Union[str, DataSourcesTreatmentAndRepresentativenessId] = None
    referenceToDataSource: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()
    useAdviceForDataSet: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()
    otherDSTAR: Optional[Union[dict, "DSTAROtherRoot"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataSourcesTreatmentAndRepresentativenessId):
            self.id = DataSourcesTreatmentAndRepresentativenessId(self.id)

        self._normalize_inlined_as_list(slot_name="referenceToDataSource", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="useAdviceForDataSet", slot_type=MultiLangString, key_name="id", keyed=True)

        if self.otherDSTAR is not None and not isinstance(self.otherDSTAR, DSTAROtherRoot):
            self.otherDSTAR = DSTAROtherRoot(**as_dict(self.otherDSTAR))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ValidationInfo(YAMLRoot):
    """
    Represents the validation information, including review entries.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ValidationInfo"]
    class_class_curie: ClassVar[str] = "ILCDmav:ValidationInfo"
    class_name: ClassVar[str] = "ValidationInfo"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ValidationInfo

    id: Union[str, ValidationInfoId] = None
    review: Optional[Union[Dict[Union[str, ReviewEntryId], Union[dict, "ReviewEntry"]], List[Union[dict, "ReviewEntry"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ValidationInfoId):
            self.id = ValidationInfoId(self.id)

        self._normalize_inlined_as_list(slot_name="review", slot_type=ReviewEntry, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReviewEntry(YAMLRoot):
    """
    A single review entry containing reviewer/institution details.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ReviewEntry"]
    class_class_curie: ClassVar[str] = "ILCDmav:ReviewEntry"
    class_name: ClassVar[str] = "ReviewEntry"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ReviewEntry

    id: Union[str, ReviewEntryId] = None
    reviewDetails: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()
    referenceToNameOfReviewerAndInstitution: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()
    referenceToCompleteReviewReport: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()
    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReviewEntryId):
            self.id = ReviewEntryId(self.id)

        self._normalize_inlined_as_list(slot_name="reviewDetails", slot_type=MultiLangString, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="referenceToNameOfReviewerAndInstitution", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="referenceToCompleteReviewReport", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ComplianceDeclarations(YAMLRoot):
    """
    Container for compliance-related declarations.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ComplianceDeclarations"]
    class_class_curie: ClassVar[str] = "ILCDmav:ComplianceDeclarations"
    class_name: ClassVar[str] = "ComplianceDeclarations"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ComplianceDeclarations

    id: Union[str, ComplianceDeclarationsId] = None
    compliance: Optional[Union[Dict[Union[str, ComplianceEntryId], Union[dict, "ComplianceEntry"]], List[Union[dict, "ComplianceEntry"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ComplianceDeclarationsId):
            self.id = ComplianceDeclarationsId(self.id)

        self._normalize_inlined_as_list(slot_name="compliance", slot_type=ComplianceEntry, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ComplianceEntry(YAMLRoot):
    """
    Holds a reference to a specific compliance system.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ComplianceEntry"]
    class_class_curie: ClassVar[str] = "ILCDmav:ComplianceEntry"
    class_name: ClassVar[str] = "ComplianceEntry"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ComplianceEntry

    id: Union[str, ComplianceEntryId] = None
    referenceToComplianceSystem: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()
    approvalOfOverallCompliance: Optional[str] = None
    nomenclatureCompliance: Optional[str] = None
    methodologicalCompliance: Optional[str] = None
    reviewCompliance: Optional[str] = None
    documentationCompliance: Optional[str] = None
    qualityCompliance: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ComplianceEntryId):
            self.id = ComplianceEntryId(self.id)

        self._normalize_inlined_as_list(slot_name="referenceToComplianceSystem", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        if self.approvalOfOverallCompliance is not None and not isinstance(self.approvalOfOverallCompliance, str):
            self.approvalOfOverallCompliance = str(self.approvalOfOverallCompliance)

        if self.nomenclatureCompliance is not None and not isinstance(self.nomenclatureCompliance, str):
            self.nomenclatureCompliance = str(self.nomenclatureCompliance)

        if self.methodologicalCompliance is not None and not isinstance(self.methodologicalCompliance, str):
            self.methodologicalCompliance = str(self.methodologicalCompliance)

        if self.reviewCompliance is not None and not isinstance(self.reviewCompliance, str):
            self.reviewCompliance = str(self.reviewCompliance)

        if self.documentationCompliance is not None and not isinstance(self.documentationCompliance, str):
            self.documentationCompliance = str(self.documentationCompliance)

        if self.qualityCompliance is not None and not isinstance(self.qualityCompliance, str):
            self.qualityCompliance = str(self.qualityCompliance)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DSTAROtherRoot(YAMLRoot):
    """
    Self-contained container for the otherDSTAR section.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["DSTAROtherRoot"]
    class_class_curie: ClassVar[str] = "ILCDmav:DSTAROtherRoot"
    class_name: ClassVar[str] = "DSTAROtherRoot"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.DSTAROtherRoot

    id: Union[str, DSTAROtherRootId] = None
    aniesDSTAR: Optional[Union[Dict[Union[str, DSTAREntryId], Union[dict, "DSTAREntry"]], List[Union[dict, "DSTAREntry"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DSTAROtherRootId):
            self.id = DSTAROtherRootId(self.id)

        self._normalize_inlined_as_list(slot_name="aniesDSTAR", slot_type=DSTAREntry, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DSTAREntry(YAMLRoot):
    """
    One entry in the otherDSTAR array. Has a 'name' and a typed 'value'.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["DSTAREntry"]
    class_class_curie: ClassVar[str] = "ILCDmav:DSTAREntry"
    class_name: ClassVar[str] = "DSTAREntry"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.DSTAREntry

    id: Union[str, DSTAREntryId] = None
    name: Optional[str] = None
    valueDSTAR: Optional[Union[dict, "DSTARReference"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DSTAREntryId):
            self.id = DSTAREntryId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.valueDSTAR is not None and not isinstance(self.valueDSTAR, DSTARReference):
            self.valueDSTAR = DSTARReference(**as_dict(self.valueDSTAR))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DSTARReference(YAMLRoot):
    """
    The typed structure that appears under 'value' in each otherDSTAR entry.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["DSTARReference"]
    class_class_curie: ClassVar[str] = "ILCDmav:DSTARReference"
    class_name: ClassVar[str] = "DSTARReference"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.DSTARReference

    id: Union[str, DSTARReferenceId] = None
    shortDescriptionExtended: Optional[Union[dict, "ExtendedMultiLangString"]] = None
    versionDict: Optional[Union[dict, "VersionDict"]] = None
    type: Optional[str] = None
    uuidDict: Optional[Union[dict, "UUIDDict"]] = None
    refObjectId: Optional[str] = None
    versionAsString: Optional[str] = None
    resourceURLs: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DSTARReferenceId):
            self.id = DSTARReferenceId(self.id)

        if self.shortDescriptionExtended is not None and not isinstance(self.shortDescriptionExtended, ExtendedMultiLangString):
            self.shortDescriptionExtended = ExtendedMultiLangString(**as_dict(self.shortDescriptionExtended))

        if self.versionDict is not None and not isinstance(self.versionDict, VersionDict):
            self.versionDict = VersionDict(**as_dict(self.versionDict))

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.uuidDict is not None and not isinstance(self.uuidDict, UUIDDict):
            self.uuidDict = UUIDDict(**as_dict(self.uuidDict))

        if self.refObjectId is not None and not isinstance(self.refObjectId, str):
            self.refObjectId = str(self.refObjectId)

        if self.versionAsString is not None and not isinstance(self.versionAsString, str):
            self.versionAsString = str(self.versionAsString)

        if not isinstance(self.resourceURLs, list):
            self.resourceURLs = [self.resourceURLs] if self.resourceURLs is not None else []
        self.resourceURLs = [v if isinstance(v, str) else str(v) for v in self.resourceURLs]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExtendedMultiLangString(YAMLRoot):
    """
    Extended multi-language string with a default value and additional language strings.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ExtendedMultiLangString"]
    class_class_curie: ClassVar[str] = "ILCDmav:ExtendedMultiLangString"
    class_name: ClassVar[str] = "ExtendedMultiLangString"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ExtendedMultiLangString

    id: Union[str, ExtendedMultiLangStringId] = None
    value: Optional[str] = None
    defaultValue: Optional[str] = None
    lstrings: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExtendedMultiLangStringId):
            self.id = ExtendedMultiLangStringId(self.id)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.defaultValue is not None and not isinstance(self.defaultValue, str):
            self.defaultValue = str(self.defaultValue)

        self._normalize_inlined_as_list(slot_name="lstrings", slot_type=MultiLangString, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class VersionDict(YAMLRoot):
    """
    Structured version information.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["VersionDict"]
    class_class_curie: ClassVar[str] = "ILCDmav:VersionDict"
    class_name: ClassVar[str] = "VersionDict"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.VersionDict

    id: Union[str, VersionDictId] = None
    versionInt: Optional[int] = None
    majorVersion: Optional[int] = None
    minorVersion: Optional[int] = None
    subMinorVersion: Optional[int] = None
    zero: Optional[Union[bool, Bool]] = None
    versionString: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, VersionDictId):
            self.id = VersionDictId(self.id)

        if self.versionInt is not None and not isinstance(self.versionInt, int):
            self.versionInt = int(self.versionInt)

        if self.majorVersion is not None and not isinstance(self.majorVersion, int):
            self.majorVersion = int(self.majorVersion)

        if self.minorVersion is not None and not isinstance(self.minorVersion, int):
            self.minorVersion = int(self.minorVersion)

        if self.subMinorVersion is not None and not isinstance(self.subMinorVersion, int):
            self.subMinorVersion = int(self.subMinorVersion)

        if self.zero is not None and not isinstance(self.zero, Bool):
            self.zero = Bool(self.zero)

        if self.versionString is not None and not isinstance(self.versionString, str):
            self.versionString = str(self.versionString)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class UUIDDict(YAMLRoot):
    """
    A wrapper for a UUID value provided as a dictionary.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["UUIDDict"]
    class_class_curie: ClassVar[str] = "ILCDmav:UUIDDict"
    class_name: ClassVar[str] = "UUIDDict"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.UUIDDict

    id: Union[str, UUIDDictId] = None
    uuidValue: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UUIDDictId):
            self.id = UUIDDictId(self.id)

        if self.uuidValue is not None and not isinstance(self.uuidValue, str):
            self.uuidValue = str(self.uuidValue)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.LCIMethodAndAllocation = Slot(uri=ILCDMAV.LCIMethodAndAllocation, name="LCIMethodAndAllocation", curie=ILCDMAV.curie('LCIMethodAndAllocation'),
                   model_uri=ILCDMAV.LCIMethodAndAllocation, domain=None, range=Optional[Union[dict, LCIMethodAndAllocationEntry]])

slots.dataSourcesTreatmentAndRepresentativeness = Slot(uri=ILCDMAV.dataSourcesTreatmentAndRepresentativeness, name="dataSourcesTreatmentAndRepresentativeness", curie=ILCDMAV.curie('dataSourcesTreatmentAndRepresentativeness'),
                   model_uri=ILCDMAV.dataSourcesTreatmentAndRepresentativeness, domain=None, range=Optional[Union[dict, DataSourcesTreatmentAndRepresentativeness]])

slots.validationInfo = Slot(uri=ILCDMAV.validationInfo, name="validationInfo", curie=ILCDMAV.curie('validationInfo'),
                   model_uri=ILCDMAV.validationInfo, domain=None, range=Optional[Union[dict, ValidationInfo]])

slots.complianceDeclarations = Slot(uri=ILCDMAV.complianceDeclarations, name="complianceDeclarations", curie=ILCDMAV.curie('complianceDeclarations'),
                   model_uri=ILCDMAV.complianceDeclarations, domain=None, range=Optional[Union[dict, ComplianceDeclarations]])

slots.otherMAV = Slot(uri=ILCDMAV.otherMAV, name="otherMAV", curie=ILCDMAV.curie('otherMAV'),
                   model_uri=ILCDMAV.otherMAV, domain=None, range=Optional[Union[dict, OtherContent]])

slots.typeOfDataSet = Slot(uri=ILCDMAV.typeOfDataSet, name="typeOfDataSet", curie=ILCDMAV.curie('typeOfDataSet'),
                   model_uri=ILCDMAV.typeOfDataSet, domain=None, range=Optional[str])

slots.referenceToLCAMethodDetails = Slot(uri=ILCDMAV.referenceToLCAMethodDetails, name="referenceToLCAMethodDetails", curie=ILCDMAV.curie('referenceToLCAMethodDetails'),
                   model_uri=ILCDMAV.referenceToLCAMethodDetails, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.otherMAA = Slot(uri=ILCDMAV.otherMAA, name="otherMAA", curie=ILCDMAV.curie('otherMAA'),
                   model_uri=ILCDMAV.otherMAA, domain=None, range=Optional[Union[dict, OtherContent]])

slots.referenceToDataSource = Slot(uri=ILCDMAV.referenceToDataSource, name="referenceToDataSource", curie=ILCDMAV.curie('referenceToDataSource'),
                   model_uri=ILCDMAV.referenceToDataSource, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.useAdviceForDataSet = Slot(uri=ILCDMAV.useAdviceForDataSet, name="useAdviceForDataSet", curie=ILCDMAV.curie('useAdviceForDataSet'),
                   model_uri=ILCDMAV.useAdviceForDataSet, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.otherDSTAR = Slot(uri=ILCDMAV.otherDSTAR, name="otherDSTAR", curie=ILCDMAV.curie('otherDSTAR'),
                   model_uri=ILCDMAV.otherDSTAR, domain=None, range=Optional[Union[dict, DSTAROtherRoot]])

slots.aniesDSTAR = Slot(uri=ILCDMAV.aniesDSTAR, name="aniesDSTAR", curie=ILCDMAV.curie('aniesDSTAR'),
                   model_uri=ILCDMAV.aniesDSTAR, domain=None, range=Optional[Union[Dict[Union[str, DSTAREntryId], Union[dict, DSTAREntry]], List[Union[dict, DSTAREntry]]]])

slots.valueDSTAR = Slot(uri=ILCDMAV.valueDSTAR, name="valueDSTAR", curie=ILCDMAV.curie('valueDSTAR'),
                   model_uri=ILCDMAV.valueDSTAR, domain=None, range=Optional[Union[dict, DSTARReference]])

slots.shortDescriptionExtended = Slot(uri=ILCDMAV.shortDescriptionExtended, name="shortDescriptionExtended", curie=ILCDMAV.curie('shortDescriptionExtended'),
                   model_uri=ILCDMAV.shortDescriptionExtended, domain=None, range=Optional[Union[dict, ExtendedMultiLangString]])

slots.versionDict = Slot(uri=ILCDMAV.versionDict, name="versionDict", curie=ILCDMAV.curie('versionDict'),
                   model_uri=ILCDMAV.versionDict, domain=None, range=Optional[Union[dict, VersionDict]])

slots.versionAsString = Slot(uri=ILCDMAV.versionAsString, name="versionAsString", curie=ILCDMAV.curie('versionAsString'),
                   model_uri=ILCDMAV.versionAsString, domain=None, range=Optional[str])

slots.resourceURLs = Slot(uri=ILCDMAV.resourceURLs, name="resourceURLs", curie=ILCDMAV.curie('resourceURLs'),
                   model_uri=ILCDMAV.resourceURLs, domain=None, range=Optional[Union[str, List[str]]])

slots.defaultValue = Slot(uri=ILCDMAV.defaultValue, name="defaultValue", curie=ILCDMAV.curie('defaultValue'),
                   model_uri=ILCDMAV.defaultValue, domain=None, range=Optional[str])

slots.lstrings = Slot(uri=ILCDMAV.lstrings, name="lstrings", curie=ILCDMAV.curie('lstrings'),
                   model_uri=ILCDMAV.lstrings, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.versionInt = Slot(uri=ILCDMAV.versionInt, name="versionInt", curie=ILCDMAV.curie('versionInt'),
                   model_uri=ILCDMAV.versionInt, domain=None, range=Optional[int])

slots.majorVersion = Slot(uri=ILCDMAV.majorVersion, name="majorVersion", curie=ILCDMAV.curie('majorVersion'),
                   model_uri=ILCDMAV.majorVersion, domain=None, range=Optional[int])

slots.minorVersion = Slot(uri=ILCDMAV.minorVersion, name="minorVersion", curie=ILCDMAV.curie('minorVersion'),
                   model_uri=ILCDMAV.minorVersion, domain=None, range=Optional[int])

slots.subMinorVersion = Slot(uri=ILCDMAV.subMinorVersion, name="subMinorVersion", curie=ILCDMAV.curie('subMinorVersion'),
                   model_uri=ILCDMAV.subMinorVersion, domain=None, range=Optional[int])

slots.zero = Slot(uri=ILCDMAV.zero, name="zero", curie=ILCDMAV.curie('zero'),
                   model_uri=ILCDMAV.zero, domain=None, range=Optional[Union[bool, Bool]])

slots.versionString = Slot(uri=ILCDMAV.versionString, name="versionString", curie=ILCDMAV.curie('versionString'),
                   model_uri=ILCDMAV.versionString, domain=None, range=Optional[str])

slots.uuidValue = Slot(uri=ILCDMAV.uuidValue, name="uuidValue", curie=ILCDMAV.curie('uuidValue'),
                   model_uri=ILCDMAV.uuidValue, domain=None, range=Optional[str])

slots.uuidDict = Slot(uri=ILCDMAV.uuidDict, name="uuidDict", curie=ILCDMAV.curie('uuidDict'),
                   model_uri=ILCDMAV.uuidDict, domain=None, range=Optional[Union[dict, UUIDDict]])

slots.review = Slot(uri=ILCDMAV.review, name="review", curie=ILCDMAV.curie('review'),
                   model_uri=ILCDMAV.review, domain=None, range=Optional[Union[Dict[Union[str, ReviewEntryId], Union[dict, ReviewEntry]], List[Union[dict, ReviewEntry]]]])

slots.referenceToCompleteReviewReport = Slot(uri=ILCDMAV.referenceToCompleteReviewReport, name="referenceToCompleteReviewReport", curie=ILCDMAV.curie('referenceToCompleteReviewReport'),
                   model_uri=ILCDMAV.referenceToCompleteReviewReport, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.referenceToNameOfReviewerAndInstitution = Slot(uri=ILCDMAV.referenceToNameOfReviewerAndInstitution, name="referenceToNameOfReviewerAndInstitution", curie=ILCDMAV.curie('referenceToNameOfReviewerAndInstitution'),
                   model_uri=ILCDMAV.referenceToNameOfReviewerAndInstitution, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.reviewDetails = Slot(uri=ILCDMAV.reviewDetails, name="reviewDetails", curie=ILCDMAV.curie('reviewDetails'),
                   model_uri=ILCDMAV.reviewDetails, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.compliance = Slot(uri=ILCDMAV.compliance, name="compliance", curie=ILCDMAV.curie('compliance'),
                   model_uri=ILCDMAV.compliance, domain=None, range=Optional[Union[Dict[Union[str, ComplianceEntryId], Union[dict, ComplianceEntry]], List[Union[dict, ComplianceEntry]]]])

slots.referenceToComplianceSystem = Slot(uri=ILCDMAV.referenceToComplianceSystem, name="referenceToComplianceSystem", curie=ILCDMAV.curie('referenceToComplianceSystem'),
                   model_uri=ILCDMAV.referenceToComplianceSystem, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.approvalOfOverallCompliance = Slot(uri=ILCDMAV.approvalOfOverallCompliance, name="approvalOfOverallCompliance", curie=ILCDMAV.curie('approvalOfOverallCompliance'),
                   model_uri=ILCDMAV.approvalOfOverallCompliance, domain=None, range=Optional[str])

slots.nomenclatureCompliance = Slot(uri=ILCDMAV.nomenclatureCompliance, name="nomenclatureCompliance", curie=ILCDMAV.curie('nomenclatureCompliance'),
                   model_uri=ILCDMAV.nomenclatureCompliance, domain=None, range=Optional[str])

slots.methodologicalCompliance = Slot(uri=ILCDMAV.methodologicalCompliance, name="methodologicalCompliance", curie=ILCDMAV.curie('methodologicalCompliance'),
                   model_uri=ILCDMAV.methodologicalCompliance, domain=None, range=Optional[str])

slots.reviewCompliance = Slot(uri=ILCDMAV.reviewCompliance, name="reviewCompliance", curie=ILCDMAV.curie('reviewCompliance'),
                   model_uri=ILCDMAV.reviewCompliance, domain=None, range=Optional[str])

slots.documentationCompliance = Slot(uri=ILCDMAV.documentationCompliance, name="documentationCompliance", curie=ILCDMAV.curie('documentationCompliance'),
                   model_uri=ILCDMAV.documentationCompliance, domain=None, range=Optional[str])

slots.qualityCompliance = Slot(uri=ILCDMAV.qualityCompliance, name="qualityCompliance", curie=ILCDMAV.curie('qualityCompliance'),
                   model_uri=ILCDMAV.qualityCompliance, domain=None, range=Optional[str])
