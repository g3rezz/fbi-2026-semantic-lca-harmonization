# Generated from linkml_administrativeInformation_schema.yaml by LinkML PythonGenerator.
# Regenerate with: ilcd-harmonizer generate-linkml
# id: https://example.org/ILCDadministrativeInformation
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

from . linkml_shared_definitions import GlobalReferenceType, GlobalReferenceTypeId, MultiLangString, MultiLangStringId, OtherContent, OtherContentId, UnixTimestamp
from linkml_runtime.linkml_model.types import Boolean, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ILCDADMIN = CurieNamespace('ILCDadmin', 'https://example.org/ILCDadministrativeInformation/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = ILCDADMIN


# Types

# Class references
class AdministrativeInformationId(extended_str):
    pass


class CommissionerAndGoalId(extended_str):
    pass


class DataGeneratorId(extended_str):
    pass


class DataEntryById(extended_str):
    pass


class PublicationAndOwnershipId(extended_str):
    pass


@dataclass(repr=False)
class AdministrativeInformation(YAMLRoot):
    """
    Container for the administrativeInformation section.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDADMIN["AdministrativeInformation"]
    class_class_curie: ClassVar[str] = "ILCDadmin:AdministrativeInformation"
    class_name: ClassVar[str] = "AdministrativeInformation"
    class_model_uri: ClassVar[URIRef] = ILCDADMIN.AdministrativeInformation

    id: Union[str, AdministrativeInformationId] = None
    commissionerAndGoal: Optional[Union[dict, "CommissionerAndGoal"]] = None
    dataGenerator: Optional[Union[dict, "DataGenerator"]] = None
    dataEntryBy: Optional[Union[dict, "DataEntryBy"]] = None
    publicationAndOwnership: Optional[Union[dict, "PublicationAndOwnership"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AdministrativeInformationId):
            self.id = AdministrativeInformationId(self.id)

        if self.commissionerAndGoal is not None and not isinstance(self.commissionerAndGoal, CommissionerAndGoal):
            self.commissionerAndGoal = CommissionerAndGoal(**as_dict(self.commissionerAndGoal))

        if self.dataGenerator is not None and not isinstance(self.dataGenerator, DataGenerator):
            self.dataGenerator = DataGenerator(**as_dict(self.dataGenerator))

        if self.dataEntryBy is not None and not isinstance(self.dataEntryBy, DataEntryBy):
            self.dataEntryBy = DataEntryBy(**as_dict(self.dataEntryBy))

        if self.publicationAndOwnership is not None and not isinstance(self.publicationAndOwnership, PublicationAndOwnership):
            self.publicationAndOwnership = PublicationAndOwnership(**as_dict(self.publicationAndOwnership))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CommissionerAndGoal(YAMLRoot):
    """
    Holds the reference about the goal and scope of the dataset.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDADMIN["CommissionerAndGoal"]
    class_class_curie: ClassVar[str] = "ILCDadmin:CommissionerAndGoal"
    class_name: ClassVar[str] = "CommissionerAndGoal"
    class_model_uri: ClassVar[URIRef] = ILCDADMIN.CommissionerAndGoal

    id: Union[str, CommissionerAndGoalId] = None
    referenceToCommissioner: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CommissionerAndGoalId):
            self.id = CommissionerAndGoalId(self.id)

        self._normalize_inlined_as_list(slot_name="referenceToCommissioner", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataGenerator(YAMLRoot):
    """
    Holds the reference to the person or entity generating the dataset.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDADMIN["DataGenerator"]
    class_class_curie: ClassVar[str] = "ILCDadmin:DataGenerator"
    class_name: ClassVar[str] = "DataGenerator"
    class_model_uri: ClassVar[URIRef] = ILCDADMIN.DataGenerator

    id: Union[str, DataGeneratorId] = None
    referenceToPersonOrEntityGeneratingTheDataSet: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataGeneratorId):
            self.id = DataGeneratorId(self.id)

        self._normalize_inlined_as_list(slot_name="referenceToPersonOrEntityGeneratingTheDataSet", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataEntryBy(YAMLRoot):
    """
    Holds timestamp and references to data set formats.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDADMIN["DataEntryBy"]
    class_class_curie: ClassVar[str] = "ILCDadmin:DataEntryBy"
    class_name: ClassVar[str] = "DataEntryBy"
    class_model_uri: ClassVar[URIRef] = ILCDADMIN.DataEntryBy

    id: Union[str, DataEntryById] = None
    timeStamp: Optional[int] = None
    referenceToDataSetFormat: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()
    referenceToPersonOrEntityEnteringTheData: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataEntryById):
            self.id = DataEntryById(self.id)

        if self.timeStamp is not None and not isinstance(self.timeStamp, int):
            self.timeStamp = int(self.timeStamp)

        self._normalize_inlined_as_list(slot_name="referenceToDataSetFormat", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="referenceToPersonOrEntityEnteringTheData", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PublicationAndOwnership(YAMLRoot):
    """
    Contains dataset version, ownership references, etc.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDADMIN["PublicationAndOwnership"]
    class_class_curie: ClassVar[str] = "ILCDadmin:PublicationAndOwnership"
    class_name: ClassVar[str] = "PublicationAndOwnership"
    class_model_uri: ClassVar[URIRef] = ILCDADMIN.PublicationAndOwnership

    id: Union[str, PublicationAndOwnershipId] = None
    dataSetVersion: str = None
    referenceToPrecedingDataSetVersion: Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]] = empty_dict()
    referenceToRegistrationAuthority: Optional[Union[dict, GlobalReferenceType]] = None
    dateOfLastRevision: Optional[int] = None
    registrationNumber: Optional[str] = None
    referenceToOwnershipOfDataSet: Optional[Union[dict, GlobalReferenceType]] = None
    copyright: Optional[Union[bool, Bool]] = None
    licenseType: Optional[str] = None
    accessRestrictions: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]] = empty_dict()
    otherPAO: Optional[Union[dict, OtherContent]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PublicationAndOwnershipId):
            self.id = PublicationAndOwnershipId(self.id)

        if self._is_empty(self.dataSetVersion):
            self.MissingRequiredField("dataSetVersion")
        if not isinstance(self.dataSetVersion, str):
            self.dataSetVersion = str(self.dataSetVersion)

        self._normalize_inlined_as_list(slot_name="referenceToPrecedingDataSetVersion", slot_type=GlobalReferenceType, key_name="id", keyed=True)

        if self.referenceToRegistrationAuthority is not None and not isinstance(self.referenceToRegistrationAuthority, GlobalReferenceType):
            self.referenceToRegistrationAuthority = GlobalReferenceType(**as_dict(self.referenceToRegistrationAuthority))

        if self.dateOfLastRevision is not None and not isinstance(self.dateOfLastRevision, int):
            self.dateOfLastRevision = int(self.dateOfLastRevision)

        if self.registrationNumber is not None and not isinstance(self.registrationNumber, str):
            self.registrationNumber = str(self.registrationNumber)

        if self.referenceToOwnershipOfDataSet is not None and not isinstance(self.referenceToOwnershipOfDataSet, GlobalReferenceType):
            self.referenceToOwnershipOfDataSet = GlobalReferenceType(**as_dict(self.referenceToOwnershipOfDataSet))

        if self.copyright is not None and not isinstance(self.copyright, Bool):
            self.copyright = Bool(self.copyright)

        if self.licenseType is not None and not isinstance(self.licenseType, str):
            self.licenseType = str(self.licenseType)

        self._normalize_inlined_as_list(slot_name="accessRestrictions", slot_type=MultiLangString, key_name="id", keyed=True)

        if self.otherPAO is not None and not isinstance(self.otherPAO, OtherContent):
            self.otherPAO = OtherContent(**as_dict(self.otherPAO))

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.commissionerAndGoal = Slot(uri=ILCDADMIN.commissionerAndGoal, name="commissionerAndGoal", curie=ILCDADMIN.curie('commissionerAndGoal'),
                   model_uri=ILCDADMIN.commissionerAndGoal, domain=None, range=Optional[Union[dict, CommissionerAndGoal]])

slots.referenceToCommissioner = Slot(uri=ILCDADMIN.referenceToCommissioner, name="referenceToCommissioner", curie=ILCDADMIN.curie('referenceToCommissioner'),
                   model_uri=ILCDADMIN.referenceToCommissioner, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.dataGenerator = Slot(uri=ILCDADMIN.dataGenerator, name="dataGenerator", curie=ILCDADMIN.curie('dataGenerator'),
                   model_uri=ILCDADMIN.dataGenerator, domain=None, range=Optional[Union[dict, DataGenerator]])

slots.dataEntryBy = Slot(uri=ILCDADMIN.dataEntryBy, name="dataEntryBy", curie=ILCDADMIN.curie('dataEntryBy'),
                   model_uri=ILCDADMIN.dataEntryBy, domain=None, range=Optional[Union[dict, DataEntryBy]])

slots.publicationAndOwnership = Slot(uri=ILCDADMIN.publicationAndOwnership, name="publicationAndOwnership", curie=ILCDADMIN.curie('publicationAndOwnership'),
                   model_uri=ILCDADMIN.publicationAndOwnership, domain=None, range=Optional[Union[dict, PublicationAndOwnership]])

slots.referenceToPersonOrEntityGeneratingTheDataSet = Slot(uri=ILCDADMIN.referenceToPersonOrEntityGeneratingTheDataSet, name="referenceToPersonOrEntityGeneratingTheDataSet", curie=ILCDADMIN.curie('referenceToPersonOrEntityGeneratingTheDataSet'),
                   model_uri=ILCDADMIN.referenceToPersonOrEntityGeneratingTheDataSet, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.timeStamp = Slot(uri=ILCDADMIN.timeStamp, name="timeStamp", curie=ILCDADMIN.curie('timeStamp'),
                   model_uri=ILCDADMIN.timeStamp, domain=None, range=Optional[int])

slots.referenceToDataSetFormat = Slot(uri=ILCDADMIN.referenceToDataSetFormat, name="referenceToDataSetFormat", curie=ILCDADMIN.curie('referenceToDataSetFormat'),
                   model_uri=ILCDADMIN.referenceToDataSetFormat, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.referenceToPersonOrEntityEnteringTheData = Slot(uri=ILCDADMIN.referenceToPersonOrEntityEnteringTheData, name="referenceToPersonOrEntityEnteringTheData", curie=ILCDADMIN.curie('referenceToPersonOrEntityEnteringTheData'),
                   model_uri=ILCDADMIN.referenceToPersonOrEntityEnteringTheData, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.dataSetVersion = Slot(uri=ILCDADMIN.dataSetVersion, name="dataSetVersion", curie=ILCDADMIN.curie('dataSetVersion'),
                   model_uri=ILCDADMIN.dataSetVersion, domain=None, range=str)

slots.referenceToPrecedingDataSetVersion = Slot(uri=ILCDADMIN.referenceToPrecedingDataSetVersion, name="referenceToPrecedingDataSetVersion", curie=ILCDADMIN.curie('referenceToPrecedingDataSetVersion'),
                   model_uri=ILCDADMIN.referenceToPrecedingDataSetVersion, domain=None, range=Optional[Union[Dict[Union[str, GlobalReferenceTypeId], Union[dict, GlobalReferenceType]], List[Union[dict, GlobalReferenceType]]]])

slots.referenceToRegistrationAuthority = Slot(uri=ILCDADMIN.referenceToRegistrationAuthority, name="referenceToRegistrationAuthority", curie=ILCDADMIN.curie('referenceToRegistrationAuthority'),
                   model_uri=ILCDADMIN.referenceToRegistrationAuthority, domain=None, range=Optional[Union[dict, GlobalReferenceType]])

slots.dateOfLastRevision = Slot(uri=ILCDADMIN.dateOfLastRevision, name="dateOfLastRevision", curie=ILCDADMIN.curie('dateOfLastRevision'),
                   model_uri=ILCDADMIN.dateOfLastRevision, domain=None, range=Optional[int])

slots.registrationNumber = Slot(uri=ILCDADMIN.registrationNumber, name="registrationNumber", curie=ILCDADMIN.curie('registrationNumber'),
                   model_uri=ILCDADMIN.registrationNumber, domain=None, range=Optional[str])

slots.referenceToOwnershipOfDataSet = Slot(uri=ILCDADMIN.referenceToOwnershipOfDataSet, name="referenceToOwnershipOfDataSet", curie=ILCDADMIN.curie('referenceToOwnershipOfDataSet'),
                   model_uri=ILCDADMIN.referenceToOwnershipOfDataSet, domain=None, range=Optional[Union[dict, GlobalReferenceType]])

slots.copyright = Slot(uri=ILCDADMIN.copyright, name="copyright", curie=ILCDADMIN.curie('copyright'),
                   model_uri=ILCDADMIN.copyright, domain=None, range=Optional[Union[bool, Bool]])

slots.licenseType = Slot(uri=ILCDADMIN.licenseType, name="licenseType", curie=ILCDADMIN.curie('licenseType'),
                   model_uri=ILCDADMIN.licenseType, domain=None, range=Optional[str])

slots.accessRestrictions = Slot(uri=ILCDADMIN.accessRestrictions, name="accessRestrictions", curie=ILCDADMIN.curie('accessRestrictions'),
                   model_uri=ILCDADMIN.accessRestrictions, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.otherPAO = Slot(uri=ILCDADMIN.otherPAO, name="otherPAO", curie=ILCDADMIN.curie('otherPAO'),
                   model_uri=ILCDADMIN.otherPAO, domain=None, range=Optional[Union[dict, OtherContent]])
