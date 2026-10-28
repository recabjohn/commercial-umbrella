ISO ERCTM Suite
Product Guide
October 2019 Edition

Edition – October 2019
Insurance Services Office, Inc.
545 Washington Boulevard, Jersey City, NJ 07310
Copyright & Proprietary Rights Notice:
© 2019 Insurance Services Office, Inc. All rights reserved. This material and any
software and content provided in connection with this material (“ISO Content”) are
protected by copyright and contain information and materials that are proprietary, trade
secret and confidential to Insurance Services Office, Inc. and its subsidiaries and
affiliates (“ISO”). Any printing, reprinting, production, copying, adaptation, display,
distribution, transmission, access and use of this material (or any part thereof) and
anything that may be described therein is strictly prohibited without the express written
consent of ISO, and receipt or possession of the ISO Content does not confer any right
to conduct any of the foregoing. ISO Content is furnished under license and any
access, use, copying and other activity pertaining to the ISO Content may be conducted
solely if and to the extent expressly provided under such license. The ISO Content may
not be made available to any third party. No title, ownership, right or license is
transferred hereunder.
2 ISO ERCTM Suite Product Guide

Table of Contents
Preface 4
Overview 5
Lines of Business and States Supported by ERC 5
Where to Access ERC Information 6
Components of ERC Package 7
ERC File Name Format 7
Documentation File 8
Rating Content Release Notes File 11
Readme Text File 17
Test Case File 18
Rating Content File 18
Data Structure Files 20
Rating Content Files 24
Algorithm Files 56
Policy Administration Elements 72
Line of Business Hierarchies 73
Businessowners 73
Commercial Automobile 74
Commercial Inland Marine – Filed 75
Commercial Inland Marine – Non-Filed 76
Commercial Package Policy 77
Commercial Property 78
Commercial Umbrella 79
Crime 80
Cyber 81
General Liability 82
Workers Compensation 83
3 ISO ERCTM Suite Product Guide

Preface
There are four guides that make up the product documentation for ISO Electronic
Rating ContentTM (ERCTM). This document, the ISO ERCTM Suite Product Guide,
explains each of the components of ERC – the rating content, algorithms, release notes,
readme file, and sample test case. The other three ERC guides are listed and briefly
described below.
ISO ERCTM Maintenance Guide
This guide outlines various scenarios that involve rating content changes that may occur
from one release to another and how these changes would be implemented within the
ERC product. It also describes the Automated Maintenance Feed (AMF), a single XML
file that includes the most recent changes to ISO rating data such as loss costs and
rating algorithms to facilitate the import of the changes only into a rating system.
ISO Rating Content XML Guide
This guide outlines the structure of the XML for the rating content.
ISO ERCTM On-line Help Guide
This guide explains how to work with the ERC product from the ISOnet user interface.
4 ISO ERCTM Suite Product Guide

Overview
ISO Electronic Rating Content (ERC) provides a package of rating information that
represents the ISO Commercial Lines Manual (CLM), integrating all the applicable
countrywide rules, state exceptions, loss costs, and form attachment logic for each line
of business and state that are effective at a certain point in time. This information is
available in Excel and XML formats that lay out the rating data (e.g., limits, deductibles,
advisory loss costs, and classification codes) and algorithms (e.g., form attachment
logic, statistical code assignment, rating messages, and premium development and
rating procedures) for working with the rating data so that the information can be
uploaded by carriers and vendors to integrate with any rating and policy administration
system.
Lines of Business and States Supported
ERC is available for the following lines of business in all states and jurisdictions
supported by ISO:
• Businessowners
• Commercial Automobile
• Commercial Inland Marine (Filed and Non-Filed)
• Commercial Package Policy
• Commercial Property
• Commercial Umbrella
• Crime
• Cyber
• General Liability
ERC also supports the following non-ISO line(s) of business:
• Workers Compensation
5 ISO ERCTM Suite Product Guide

Where to Access ERC Information
Access to ERC information, including the rating content and algorithm files, as well as
update and support information, is available through the ISOnet user interface. See the
screenshot below of the ERC home page which is the starting point for searching,
selecting, and downloading ERC information.
For more information about how to access ERC via ISOnet and set up e-mail alerts
about product updates, please refer to the ISO ERC On-Line Help Guide on the ERC
home page under the “ISO ERC Help” link.
6 ISO ERCTM Suite Product Guide

Components of ERC Package
Once an ERC or “Ratebook Content” package is opened from the search results page,
a WinZip file containing an ERC folder will be displayed. This is where all the files are
stored that make up the specific Ratebook Content package selected. See the example
below.
Once the ERC folder is opened, all the files contained in that folder will be displayed.
See the screenshot below followed by a description of the file name format and each
type of file.
ERC File Name Format
ERC files use the format TTTT-LL-XX-MMDDYYYY-VVV:
• TTTT – Identifies the type of file (e.g., ALG, AMF, DOC, RC, RCRN, and TC).
• LL – Identifies the two-character alpha code for a line of business (e.g., CF for
Commercial Property).
• XX – Identifies the two-character alpha code for a state or “CW” for countrywide.
• MM/DD/YYYY – Identifies the two-digit month and day followed by the four-digit year
representing the effective date of the rating content. Note: Effective date is driven
by the effective date of circulars that approve modifications to the ISO CLM.
• VVV – Identifies the version number of the content. Occasionally an ERC package
that has already been released to ISOnet needs to be updated to address a
correction or enhancement. Whenever this occurs, the ERC package is re-released
with a new version number.
7 ISO ERCTM Suite Product Guide

Documentation File
The documentation or “DOC” file provides information about specific ISO CLM rules and
plans that are not supported within ERC or that are “Refer to Company”. This file also
provides special considerations related to the line of business, such as rule number
guidelines and stat assignment. It is important to review this file before beginning work
with the rating content and algorithms to make sure you know what is Refer to Company
and not supported in the specific ERC package.
The DOC file is in an Excel format and contains several different worksheets or tabs.
See the list of tabs below followed by a brief description and illustration of each.
• Table of Contents
• Refer to Company
• Not Supported
• Rule Number Guideline
• Stat Assignment
• Special Considerations
Table of Contents Tab
The Table of Contents tab lists the sections of the DOC file including links to each
section. See the example below. Note: The sections included in a DOC file will vary,
depending on the ERC package. However, most DOC files include Refer to Company
and “Not Supported” tabs.
Refer to Company Rules Tab
The ISO CLM contains many Refer to Company rules. These are rules that instruct the
user to check with their company for information regarding the implementation of rating
8 ISO ERCTM Suite Product Guide

content which may be dictated or based on a company filing. For example, Rule 2.
REFERRALS TO COMPANY in the State Insurance Manual (SIM) for Commercial
Property Alabama (SIM-CF-AL-05/01/2015) states the following:
To the degree that Refer to Company rules are supported in ERC, information is
provided in the “Customer Implementation Guidelines” column of the Refer to Company
tab. See the example below.
Not Supported Rules Tab
“Not Supported” rules are rules that are not supported in ERC. For example, Rule 85.N.
Transition Rule for Changes in Class Rating Eligibility – Light Manufacturing Classes
and Hotels/Motels in the State Insurance Manual (SIM) for Commercial Property in
Alabama (SIM-CF-AL-05/01/2015) states the following:
9 ISO ERCTM Suite Product Guide

For this rule, the ERC Customer Implementation Guideline refers the user to the
company for information about how to implement this rule. See the example below.
Rule Number Guideline Tab
The “Rule Number Guideline” tab provides information about how ISO rule references
are formatted and documented within ERC. See the examples below:
Stat Assignment Tab
The “Stat Assignment” tab provides information about how stat codes are assigned
within ERC. See the example below. Note: The Page Number column refers to the
page in the ISO Statistical Manual that addresses the specific stat code.
Page
Code Assignment Number Customer Implementation Guidelines
Automobiles Rate table
Furnished for Regular PrivatePassengerAutosFurnishedForRegularUseStatCode
Use: Private CA-LI-39.2; is added and AutosFurnishedForRegularUse page field is
Passenger CA-PH-35.2 added on Private Passenger Detail page
Special Considerations Tab
The “Special Considerations” tab provides additional information regarding the line of
business that may be unique to the line and important to note during the
implementation. See the example below.
Content Special Considerations
Class codes classified under "Other Public Buses" will use the
Other Public Buses is rated same loss cost values as "Other Buses". This will be reflected in
as Other Buses the rate table PublicTransportationGroup
10 ISO ERCTM Suite Product Guide

Rating Content Release Notes (RCRN) File
The Rating Content Release Notes (RCRN) file is a Word document that describes in
detail the changes made within a specific ERC package as of the effective date
identified in the RCRN file name. The types of changes that can be made to an ERC
package include approved changes announced in ISO Circulars, as well as corrections,
enhancements, and maintenance items. It is important to review release notes to be
aware of changes made to the rating content and algorithms for implementation, as well
as maintenance purposes.
Depending on the effective date of the ERC package, there can be one or two RCRN
files. ERC packages released prior to June 2014 contain state and countrywide files
bundled together in a single ERC package and two RCRN document files, one
countrywide version and one state version. See the example below.
ERC packages released after June 2014 split state and countrywide files into separate
ERC packages each with its own RCRN file. Countrywide ERC packages include a
countrywide version of the release notes; state ERC packages include a state-specific
version. See the example below.
Also, as of February 2016, changes to values made in the rate tables and domain tables
found in the Rating Content (“RC”) file and changes to PCH and workflow changes
found in the Algorithm (“ALG”) file are available in an XML format. This information is
stored in a separate maintenance file called the “AMF” (Automated Maintenance Feed)
11 ISO ERCTM Suite Product Guide

file. Please refer to the ISO ERC Maintenance Guide for more information about this
XML file.
See a list of release notes sections below followed by a description and illustration of
each:
• Table of Contents
• Release Information
− Countrywide Release Information
− Version History
− Circular Reference(s)
− Latest Circulars by Service Type
• Changes in this Release
− Circular Implementations
− Enhancements
− Corrections
− Maintenance
• Known Issues
• Items to Update
• Special Considerations
• Support
Table of Contents – The table of contents summarizes the sections of the release
notes. Below is a screenshot of the table of contents page for the release notes
contained in the Commercial Property countrywide package, RC-CF-CW-05012015-
V02.
12 ISO ERCTM Suite Product Guide

Countrywide Release Information - This section identifies the name and effective date
of the ERC package being released and also provides other information pertinent to the
release including version history, circular references, and the latest circulars by service
type. See the example below.
As the example shows, this is a second version of the countrywide content which is
denoted by “V02” in the file name. Whenever a file is re-released with changes to the
content, the file is assigned a new version number. All the items contained within the
CF-CW-05012015-V01 release also apply to CF-CW-05012015-V02, as well as the new
items added. Note: Throughout the release notes document, the text highlighted in
blue font identifies information about the new items added to a release.
13 ISO ERCTM Suite Product Guide

Version History – This section identifies the date each version of the content was
released to ISOnet. See the example below. In this case, CF-CW-05012015-V01 was
released to ISOnet on 10/18/2014 and CF-CW-05012015-V02 was released on
2/19/2015.
Circular Reference(s) - This section summarizes information about the ISO Circulars
that are being implemented in the ERC package including the ISO Circular name,
number, date released, and type, as well as the corresponding Filing ID or Filing
Reference number and Notice to Manualholders (NTM) number. See the example
below.
Latest Circulars by Service Type - This section identifies the most recent ISO
Circulars that have been implemented by service (ISO Loss Costs, Rules, Forms, and
Statistical Plan), as well as the effective date for each type of circular. See the example
below.
Changes in this Release – This section describes the changes within the ERC
package including all circular implementations, as well as corrections, enhancements,
and maintenance items.
14 ISO ERCTM Suite Product Guide

Circular Implementations - This section provides a detailed list of the changes
associated with the ISO Circular that were implemented in the ERC package.
Examples of changes include the addition, revision, or deletion of Tables, Columns,
Pages, Page Fields, Domain Tables, and Rate Tables, as well as changes to
algorithms. See the example below.
Enhancements - This section provides detailed information about any enhancements
implemented in the ERC package. See the example below.
Corrections - This section provides detailed information about any corrections made to
the ERC package including a brief description of the problem and the solution. See the
example below.
15 ISO ERCTM Suite Product Guide

Maintenance – This section provides detailed information about any maintenance items
included in the release. See the example below.
Known Issues - This section identifies any known issues being released in the ERC
package.
Support - This section provides a link to the ERC Customer Support Portal where
cases concerning questions or issues are created and submitted to the ERC Support
Team.
Release Notes for State ERC Packages
All the sections described above for the countrywide RCRN document are contained in
the state RCRN file, as well as a section for State Release Information. This section
identifies the name and effective date of the state package. See the example below.
16 ISO ERCTM Suite Product Guide

Readme Text File
For information purposes, a generic Readme Text file is distributed with every ERC
package. This file contains a list and brief description of all the files distributed within an
ERC package including countrywide, state, Excel, XML, and human readable (HR), and
machine readable (MR) versions of the files. See the example below. This information
may be used for audit purposes, i.e., every file identified in the Readme file should be
included in the ERC package you are working with.
17 ISO ERCTM Suite Product Guide

Test Case (TC) File
Every state ERC package includes a Test Case (TC) file that provides a sample test
case. The sample test case is an Excel representation of a policy that outlines the data
used at each risk level and the sub premiums and total premium generated from this
data.
Below is a list and brief description of the worksheets or tabs within the TC file followed
by an illustration.
• Input - Provides the data or values used in the test case policy.
• Calculations - Provides the premiums.
Rating Content (RC) File
The Rating Content or “RC” file contains all the rating data (e.g., limits, deductibles,
advisory loss costs, and classification codes) and requirements (e.g., domain tables) for
a line of business. This information is provided in both Excel and XML formats. See the
example of the RC files below for Commercial Property countrywide content effective
05-01-02015 (CF-CW-05012015-V02).
18 ISO ERCTM Suite Product Guide

If you are involved in building an interface or tool to programmatically consume ERC
into a rating system, you will most likely work with the XML format which provides a
machine-readable version of the RC file; otherwise, you should work with the Excel
format.
Except for Commercial Auto and General Liability, countrywide rating content is
provided in two files, as shown above. However, for Commercial Auto and General
Liability there are four files, two countrywide or “CW1” files and two “CW2” files. See
the example below.
If you are working with the rating content for Commercial Auto or General Liability, in
your initial analysis of the content, you will need to work with both the CW1 and CW2
files to get a complete picture of the line of business. Once you have completed your
initial analysis, you will only need to work with the CW2 file for maintenance purposes.
While the countrywide RC file provides two files, the RC file for state content provides
four files – two “RC” files and two “DS” files. See the example below.
19 ISO ERCTM Suite Product Guide

Data Structure (DS) Files
The “DS” or data structure files provide an overview of the line of business, as of the
effective date of the content (e.g., 05-01-2015). All the tables involved in building the
structure of the line of business are in this file including active and obsolete tables at the
countrywide and state levels. In addition, this file illustrates the relationship of these
tables, i.e., the parent/child relationship.
The reason why the DS files are included in the state file and not the countrywide file is
because countrywide files do not change once they are released whereas state files
typically involve changes.
Below is a list and brief description of the tabs within the DS file.
• Tables
• Column Details
• Ratebook Tables
DS File - Tables Tab
The Tables tab provides a list of all the tables that make up the line of business and the
parent/child relationship these tables have to one another. See the example below
followed by a brief description of each column.
• Table - Provides the name of the table.
• Parent - Represents the relationship the table has to other tables. In the example
above, the “Commercial Property” table is the parent of the “Commercial Property
Additional Locations Special Coinsurance General Information” table.
• Description - Provides a brief description of the table.
• Type - Identifies the type of table. There are five types. See diagram and
description of each below.
20 ISO ERCTM Suite Product Guide

Policy Page
Policy Level Policy Level Risk
Forms Coverages
Form Risk Level Risk Level Risk
Coverages Forms Coverages
Form
Coverages
Types of Tables:
1. Policy – The policy level represents the policy table in the rating content database.
There can only be one policy per record; this is the starting point of the hierarchy of
rating content. The following items can be linked to a record at the policy level:
a. One or more risks
b. Zero or more forms
c. Zero or more coverages
2. Risk – Each risk represents a risk table in the rating content database. Examples of
risks include vehicles on a Commercial Auto policy or locations and buildings on a
Businessowners policy. There can also be zero or more child risks associated with
a parent risk. The following items can be linked to each record at the risk level:
a. Zero or more child risks
b. Zero or more forms
c. Zero or more coverages
d. Zero or more schedules (not shown in diagram for clarity)
3. Form - Each form represents a form table in the rating content database. There can
be zero or more forms associated with a policy record or with a risk. Examples of
forms include Audio Equipment and Driver Exclusion on a Commercial Auto policy.
The following items can be linked to each record at the form level:
a. Zero or more coverages
b. Zero or more schedules
4. Coverage - Each coverage represents a coverage table in the rating content
database. There can be zero or more coverages associated with a policy record, a
risk, or a form. Examples of coverages include specific protection for Collision,
Liability, or Personal Injury on a Commercial Auto policy.
5. Schedule - Each schedule represents a schedule table in the rating content
database. An example of a schedule is a list of names for Named Individuals -
21 ISO ERCTM Suite Product Guide

Personal Injury Protection coverage on a Commercial Auto policy. There can be
zero or more schedules associated with a "scheduled" risk or form, and there can be
zero or more coverages linked to each record at the schedule level (not shown in
diagram for clarity purposes).
Note: In addition to ERC, we have another product called “ERC+software”. The following
types of tables are only used with ERC+software. Please disregard them for ERC
purposes.
1. Human
2. Company
3. Payment
4. Note
5. User
6. Address
DS File - Column Detail Tabs
Each table is assigned columns. Some are system generated and some are coverage
specific and added based on the line of business requirements from the ISO CLM. The
system generated columns provide insurance-specific support for rating. These include
items such as Effective Date, Premium, and Unit Number.
Columns can either be inputs or derived values for use within the algorithm. An
example for input would be a class code. In Commercial Auto, a class code is
represented as a column on a Truck Risk. The column “PrimaryClassCode” is
controlled by a domain table TruckPrimaryClassCode which contains the class codes
filed for the line of business in a state.
Columns can also store derived values generated by the algorithm. Continuing with the
previous example, the class code can be a determining factor in the loss cost utilized in
rating. The class code is a key to the lookup of the appropriate factor used in the rating
algorithm. For example, TruckPrimaryClassCode is the key to determining the
appropriate factor to be pulled from the loss cost table
TruckPrimaryClassLiabilityFactor. This value is then used in the algorithm to develop
and populate the column LiabilityPremium on the
CommercialAutoVehicleLiabilityCoverage table.
22 ISO ERCTM Suite Product Guide

The Column Details tab describes the entire structure of the line of business and
provides the type, size, and scale of the column. See the example below followed by a
description of each column.
There are several types of columns. These are listed and described below.
• Decimal – The information is a decimal value (e.g., used with Loss Costs, Rates, or
Premiums). With decimal data types, the size and scale values must be specified.
The standards are as follows:
o Rates and Factors - 8 size, 4 scale
o Premium - 10 size, 2 scale
• Integer - The information is an integer value (e.g., used with limits, number of
employees, or payroll). When the integer data type is specified, the size and scale
fields are not used.
• Text - The information is a text value. When the text data type is specified, the size
value must be specified.
• Unique Identifier – The information is a unique identifier and used to link tables
(e.g., used with Human, Address, or Company).
23 ISO ERCTM Suite Product Guide

Rating Content (RC) Tabs
Below is a list and brief description of the tabs within the RC file followed by an
illustration of each.
• Ratebook Properties
• Ratebook Hierarchy
• Ratebook Tables or Linked Tables
• Ratebook Columns
• Domain Tables
• Domain Table Keys
• Domain Table Entries
• Rate Tables
• Rate Table Keys
• Rate Table Value Columns
• Rate Table Entries
• Pages
• Page Fields
• Page Related Fields
Ratebook Properties Tab
The Ratebook Properties tab provides an overview of the structured content contained
within the file and identifies the Company Name, Locale, Line of Business, State,
Effective Date, and Version associated with the content. See the example below
followed by a description of the columns within the Ratebook Properties report.
• Report Type: Exceptions (Additions And Deletions) – This section indicates that
the RC file includes changes – additions and deletions. Every RC file reflects some
change to the ISO CLM that has been published and approved in an ISO Circular.
Note: Prior to August 2011, all report types were “Full” instead of “Exceptions”. Full
report types not only contain unique items per the state manual, but all inherited
values, as well:
o Inherited values are shown in black font
24 ISO ERCTM Suite Product Guide

o All unique items are shown in blue font
• Company Name – Identifies the source of the information that the rating content is
based on. The company name will be “ISO” except with Workers Compensation and
a few Commercial Auto packages where the source of information is a rating bureau.
For example, rating content for Workers Compensation in Delaware is shown as
Delaware Compensation Rating Bureau (DCRB).
• Locale - Identifies the language and country of origin for the rating content. This will
always be “English - United States”.
• Line of Business - Identifies the specific line of business that the RC file covers.
• State - Identifies the specific state that the RC file covers. Note: In a countrywide
file, this column will be blank; if you are working with a multi-state file, “XX” will be
displayed.
• New Business Effective - Indicates the effective date of the rating content.
• Renewal Effective Date - Will always match the “New Business Effective” date.
• Version - Identifies the version of the content for the given effective date. Note: If a
version is not specified, by default that means you are working with the first version
of the rating content; otherwise, you are working with whatever version number is
shown in this field.
• Published and Released - This information is used with our other product,
ERC+software; please disregard this for ERC purposes.
Ratebook Hierarchy Tab
The Ratebook Hierarchy tab outlines the hierarchy of the content in the RC file. Every
ERC package includes layers of content including non-LOB base content (information
universal to all lines of business), countrywide content, and state content if you are
working with a state release. See the example below followed by a description of the
columns within the Ratebook Hierarchy report.
• Company Name, Locale, Line of Business, and State – Provides the same
information provided for these columns in the Ratebook Properties tab. Note: In
addition to ISO, “AscendantOne” is identified in the Company Name column.
AscendantOne refers to the underlying software product used with ERC.
25 ISO ERCTM Suite Product Guide

• Title - Illustrates the hierarchy or the layers of rating content. At the top of the
hierarchy (read from the bottom up) is the non-LOB base content which contains
information universal to all lines of business such as specific domains and
constraints. Next is the countrywide layer of content which contains the information
in the multistate section of the ISO CLM. The last level is the state rating content
which contains the exceptions to the countrywide that are located in the State
Exception section of the ISO CLM.
• New Business Effective, Renewal Effective, Version, and Published – Provides
the same information provided in these columns in the Ratebook Properties tab.
• New Business Effective and Renewal Effective - Identify the effective date of the
rating content in the file which is 05012015 in the above example.
• Version - Identifies the version of the rating content. Occasionally a Rating Content
package is re-released to address a correction, out-of-sequence endorsement, or
additional approval circular. When this occurs, the rating content is assigned a new
version. If a version number is not shown in this column, this indicates you are
working with version 1; otherwise, you are working with whatever version number is
shown in this column.
The other information columns are used with our other product, ERC+software. Please
disregard them for ERC purposes.
Ratebook Tables or Linked Tables Tab
The “Ratebook Tables” or “Linked Tables” tab identifies the database tables required in
building pages and page fields and in the database tables used with ERC algorithms in
the rating process. See the example and a brief description of each column below.
26 ISO ERCTM Suite Product Guide

• Table - Identifies the name of the table.
• Linked – Identifies “Yes” or “No” indicating whether the table is utilized within the
specific ERC package. The reason why all the tables are marked “Yes” is because
behind the scenes there is an underlying database (i.e., the DS file) which contains
an inventory of all the tables for a line of business including active and obsolete
tables at the countrywide and state levels. The tables marked with a “Yes” as shown
in the above example are extracted from this database because these are the tables
used with the specific ERC package.
• Bureau Rule Number - The rule in the ISO CLM that applies to this table.
• Comment – Identifies the name of the table in the ALG Table of Contents. Note:
there may exceptions in which case these would be identified in the AG file in the
Rule Number Guideline tab.
Ratebook Columns Tab
There is a great deal of information provided within ERC, but not all the data is required
to rate a policy. The purpose of the Ratebook Columns tab is to identify the specific
information that is required for rating purposes. See the example and a brief description
of each column below.
27 ISO ERCTM Suite Product Guide

• Table - Lists all the tables involved in rating.
• Column - Identifies the specific information within a table that needs to be captured
to rate a policy.
• Rating Required – Identifies “Yes” or “No” whether the field is required in the rating
process. This means that values for these items are expected in the ALG to
generate a premium. Note: The only time you are going to see a “No”, is when the
value is needed for stat assignment.
• Rating Required Condition - Identifies conditions that determine the type of policy
that would require this field to be populated for rating purposes.
• Status – Identifies whether the column has been defined at the countrywide or state
level. This information will be utilized in the creation of a common line of business
definition while layering in state specific filing information.
Domain Table Tabs
The “Domain Table” tabs, including “Domain Tables”, “Domain Table Keys”, and
“Domain Table Entries”, are all related and work together to provide information about
the valid options available for a desired page field.
Domain Tables Tab
The “Domain Tables” tab contains a list of all domain tables applicable to the
countrywide or state rating content. See the examples below followed by a brief
description of each column within the tab.
28 ISO ERCTM Suite Product Guide

• Table – Identifies the names of all the domain tables applicable to the rating content.
• Title – Identifies the name of the table but with spacing between words.
• Type – Provides the types of values available for a page field. There are two types
of values:
1. Picklist – The domain table value is defined from a distinct list of choices and
has an exact match. See the example below.
CauseOfLoss Sequence Display Value DataValue
CauseOfLoss 1 Basic Basic
CauseOfLoss 2 Broad Broad
CauseOfLoss 3 Special Special
2. Range – The domain table value is between a minimum and maximum value and
can identify a set of ranges for an entry. See the example below.
UtilityServicesTimeElementLimit Sequence MinimumValue MaximumValue
UtilityServicesTimeElementLimit 1 1 999999999
• Data Type – Identifies the type of data allowed in populating a page field. There are
four types of data:
1. Date
2. Decimal
3. Integer
4. Text
• Size – Defines the length of a field or constraint. Note: Size is applicable only when
the data type is decimal or text.
• Scale – This constraint is only applicable to the decimal data type.
• Masked – Indicates whether the domain table is masked. Note: A masked table
changes the structure of an inherited table with the same name. Masked tables are
no longer used and are in the process of being removed.
• Bureau Rule Number – Identifies the rule in the ISO CLM that is being addressed.
The other information columns are used with our other product, ERC+software, and should
be disregarded for ERC purposes.
Domain Table Keys Tab
The “Domain Table Keys” tab provides the criteria for selections within a given table. If
a domain table does not have an associated key, all the values listed in the domain
29 ISO ERCTM Suite Product Guide

table will be available. If a domain table has one or more keys, the values that are
available are only those that match the data in the key(s).
The Domain Table Keys tab will only contain the domain tables that have at least one
key. See the example below including a brief description of each column.
• Domain Table - Lists the names of all the domain tables that have keys.
• Key - Names the specific key or constraint within the domain table.
• Sequence - Represents the order in which the keys will be used in the domain table.
• Type - Provides the types of keys -- date, decimal, integer, and text.
• Size - Defines the length of the key which is required only when the data type is
decimal or text.
• Scale - Applies only to the decimal data type.
The other information columns are used with our ERC+software product, and should be
disregarded for ERC purposes.
In the above example, the ZipCodeTN domain table has two keys -- CityTown and
County. The data for City and County needs to be provided to determine the values
that are available for the ZipCode result. Based on this example and the table below,
we can determine that when the city is Angola and the county is Steuben, then the
ZipCode values available to select are only: 46703 and Other.
30 ISO ERCTM Suite Product Guide

ZipCodeIN CityTownIN CountyIN Sequence Display Value DataValue
| ZipCodeIN | Anderson | Madison    | 28  | 46011 | 46011   |
| --------- | -------- | ---------- | --- | ----- | ------- |
| ZipCodeIN | Anderson | Madison    | 29  | 46012 | 46012   |
| ZipCodeIN | Anderson | Madison    | 30  | 46013 | 46013   |
| ZipCodeIN | Anderson | Madison    | 31  | 46014 | 46014   |
| ZipCodeIN | Anderson | Madison    | 32  | 46015 | 46015   |
| ZipCodeIN | Anderson | Madison    | 33  | 46016 | 46016   |
| ZipCodeIN | Anderson | Madison    | 34  | 46017 | 46017   |
| ZipCodeIN | Anderson | Madison    | 35  | 46018 | 46018   |
| ZipCodeIN | Anderson | Madison    | 36  | Other | Other   |
| ZipCodeIN | Anderson | Other      | 37  | Other | Other   |
| ZipCodeIN | Andrews  | Huntington | 38  | 46702 | 46702   |
| ZipCodeIN | Andrews  | Huntington | 39  | Other | Other   |
| ZipCodeIN | Andrews  | Other      | 40  | Other | Other   |
| ZipCodeIN | Angola   | Steuben    | 41  | 46703 | 46703   |
| ZipCodeIN | Angola   | Steuben    | 42  | Other | Other   |
| ZipCodeIN | Angola   | Other      | 43  | Other | Other   |

Note:  The data value “Other” means the user must key in the zip code.  This option is
used with our ERC+software product and should be disregarded for ERC purposes.

Domain Table Entries Tab

The “Domain Table Entries” tab lists all the data entry selections associated with the
applicable domain table listed in the “Domain Tables” tab.  See the example below
followed by a brief description of each column.

| 31  ISO ERCTM Suite Product Guide  |     |     |     |     |     |
| ---------------------------------- | --- | --- | --- | --- | --- |

• Key(s) - If a domain table has one or more keys, then the keys columns will be
displayed before any other element. If the domain table doesn’t have any keys, the
next element will be displayed. See the example below where Domain Table
BasicGroupIRatingTerritory has two keys, CityTown and County. These two keys
will be displayed in the order of their sequence from left to right.
Domain Table
BasicGroupIRatingTerritory CityTown County Sequence Display Value DataValue Status
Domain Table CityTownTN doesn’t have any keys. See the example below.
Domain Table
CityTownTN Sequence Display Value DataValue Status
• Sequence – Represents the order of the pick list for display purposes.
• DisplayValue – This is used for internal purposes; please disregard.
• DataValue – This is for a picklist domain table and represents the collected value.
The type of data in this column is the data type selected for the Domain Table.
• MinimumValue – This is used for a range domain table and contains the minimum
value of the defined range. The type of the data in this column is the data type
selected for the Domain Table.
• MaximumValue – This is for a range domain table and contains the maximum value
of the defined range. The type of the data in this column is the data type selected for
the Domain Table
• Status – Indicates whether an entry has been added, changed, or deleted from the
table. Once an item is either added or changed, it remains permanent with that
status until it is either deleted or re-inherited, i.e., from the countrywide. Once an
item is deleted, it remains permanent with that status until it is re-inherited from a
base or parent report.
Domain Tables – Relationship to ISO CLM
Within the rating content there are domain tables that are based on specifications within
a rule. For example, the rule table 85.M.1.b. Protection Class Multipliers in Commercial
Property Illinois has the following options for Protection Class: 1, 2, 3, 4, 5, 6, 7, 8, 8B, 9
and 10. See the example below.
32 ISO ERCTM Suite Product Guide

In the Illinois rating content, we have a domain table called “ProtectionClass” which
would contain the values listed on the rule table.  See the example below.

| ProtectionClass | Sequence | Display Value | DataValue |     |
| --------------- | -------- | ------------- | --------- | --- |
| ProtectionClass | 1        | 01            | 01        |     |
| ProtectionClass | 2        | 02            | 02        |     |
| ProtectionClass | 3        | 03            | 03        |     |
| ProtectionClass | 4        | 04            | 04        |     |
| ProtectionClass | 5        | 05            | 05        |     |
| ProtectionClass | 6        | 06            | 06        |     |
| ProtectionClass | 7        | 07            | 07        |     |
| ProtectionClass | 8        | 08            | 08        |     |
| ProtectionClass | 9        | 8B            | 8B        |     |
| ProtectionClass | 10       | 09            | 09        |     |
| ProtectionClass | 11       | 10            | 10        |     |

There are other generic domain tables that can be used for different fields.  For
example, if a field has the value of “Yes” or “No”, this field would use the “YesNo”
generic domain table containing the Yes and the No values.  See the example below.

| YesNo | Sequence | Display Value | DataValue |     |
| ----- | -------- | ------------- | --------- | --- |
| YesNo | 1        | No            | No        |     |
| YesNo | 2        | Yes           | Yes       |     |

Domain Tables – Relationship to Page Fields

Domain tables are created to be used with page fields.  We can categorize the
relationship between domain tables and page fields as follows:

•  One to One - One domain table is assigned to a page field.
33  ISO ERCTM Suite Product Guide

• One to Many - One domain table is assigned to various page fields.
However, each page field can only be linked to one domain table. Most fields in rating
content are associated with a domain table.
Some page fields utilize range domain tables for restricting input of a decimal or an
integer. For example, a Limit field that requires the input to be more than $100000
would use a range domain to restrict the value of the field to at least $100000.
A good example of how keys in a domain table work based on another page field is in
obtaining the correct Construction Code after selecting a Construction Type. In
Commercial Property, the Washington rule exception 15.B has a list of construction
definitions, as follows:
The ConstructionType page field uses a picklist domain table which contains all the
types of constructions listed in the ISO CLM. See the example below.
34 ISO ERCTM Suite Product Guide

| ConstructionTypeBldg | Sequence |     | Display Value   | DataValue       |     |
| -------------------- | -------- | --- | --------------- | --------------- | --- |
| ConstructionTypeBldg | 1        |     | Fire Resistive  | Fire Resistive  |     |
| ConstructionTypeBldg | 2        |     | Frame           | Frame           |     |
| ConstructionTypeBldg | 3        |     | Joisted Masonry | Joisted Masonry |     |
ConstructionTypeBldg 4 Masonry Non-Combustible  Masonry Non-Combustible
ConstructionTypeBldg 5 Modified Fire Resistive Modified Fire Resistive
| ConstructionTypeBldg | 6   |     | Non-Combustible | Non-Combustible |     |
| -------------------- | --- | --- | --------------- | --------------- | --- |

The value then selected for ConstructionType is passed as a key on the
ConstructionCode domain table.  Depending on the construction type, the domain table
will return the code listed for that type.  Then the code from the DataValue column
would be assigned to the ConstructionCode page field.  See the example below.

ConstructionCode ConstructionTypeToUse Sequence Display Value DataValue
| ConstructionCode | Frame                   | 1   | 1   | 1   |     |
| ---------------- | ----------------------- | --- | --- | --- | --- |
| ConstructionCode | Joisted Masonry         | 2   | 2   | 2   |     |
| ConstructionCode | Non-Combustible         | 3   | 3   | 3   |     |
| ConstructionCode | Masonry Non-Combustible | 4   | 4   | 4   |     |
| ConstructionCode | Modified Fire Resistive | 5   | 5   | 5   |     |
| ConstructionCode | Fire Resistive          | 6   | 6   | 6   |     |

Domain Tables – Relationship to Rate Tables

Domain table data values are very important in relation to rate tables.  Rate table criteria
selections are based upon domain table entries.  Most of the domain table entries are
used as keys within rate tables.   For example, in Commercial Property under the
Occupancy Class risk level the ClassCode page field uses a domain table called
ClassCodeOccupClass and the OccupCategory page field uses a Domain table called
OccupancyCategory.  See the example below.

35  ISO ERCTM Suite Product Guide

Domain Table
ClassCodeOccupClass RatingType Sequence Display Value DataValuSetatus
| ClassCodeOccupClass | Class 1                | 0074      | 0074 Added |
| ------------------- | ---------------------- | --------- | ---------- |
| ClassCodeOccupClass | Class 2                | 0075      | 0075 Added |
| ClassCodeOccupClass | Class 3                | 0076      | 0076 Added |
| ClassCodeOccupClass | Specific 100           | 0074      | 0074 Added |
| ClassCodeOccupClass | Specific 101           | 0075      | 0075 Added |
| ClassCodeOccupClass | Specific 102           | 0076      | 0076 Added |
| ClassCodeOccupClass | Tentative 236          | 0074      | 0074 Added |
| ClassCodeOccupClass | Tentative 237          | 0075      | 0075 Added |
| ClassCodeOccupClass | Tentative 238          | 0076      | 0076 Added |
| OccupancyCategory   | Sequence Display Value | DataValue | Status     |
OccupancyCategory 1 Residential Apartments and Condominiums Residential Apartments and Condominiums Added
| OccupancyCategory | 2 Offices    | Offices    | Added |
| ----------------- | ------------ | ---------- | ----- |
| OccupancyCategory | 3 Mercantile | Mercantile | Added |
OccupancyCategory 4 Motels and Hotels Motels and Hotels Added
| OccupancyCategory | 5 Institutional | Institutional | Added |
| ----------------- | --------------- | ------------- | ----- |
OccupancyCategory 6 Industrial and Processing  Industrial and Processing  Added
| OccupancyCategory | 7 Service     | Service     | Added |
| ----------------- | ------------- | ----------- | ----- |
| OccupancyCategory | 8 Contractors | Contractors | Added |

A value from these domain tables will be assigned to their respective page fields. The
values from these page fields will then be used to determine the value of
OccupCategoryRiskSeverity page field through a rate table lookup.

If the value selected for the ClassCode page field is “0074” and the value selected for
the OccupCategory page field is “Offices”, then the value that the rate table lookup will
return for OccupCategoryRiskSeverity page field will be “Not Applicable”.  See the
example below.

| 36  ISO ERCTM Suite Product Guide  |     |     |     |
| ---------------------------------- | --- | --- | --- |

Rate Table
OccupCategoryRiskSeverity OccupCategory ClassCode Severity Status
OccupCategoryRiskSeverity Contractors 0074 Not Applicable Added
OccupCategoryRiskSeverity Contractors 0075 Not Applicable Added
OccupCategoryRiskSeverity Contractors 0076 Not Applicable Added
OccupCategoryRiskSeverity Industrial and Processing  0074 Low Added
OccupCategoryRiskSeverity Industrial and Processing  0075 Low Added
OccupCategoryRiskSeverity Industrial and Processing  0076 Low Added
| OccupCategoryRiskSeverity | Institutional | 0074 Low    | Added |
| ------------------------- | ------------- | ----------- | ----- |
| OccupCategoryRiskSeverity | Institutional | 0075 Low    | Added |
| OccupCategoryRiskSeverity | Institutional | 0076 Low    | Added |
| OccupCategoryRiskSeverity | Mercantile    | 0074 Medium | Added |
| OccupCategoryRiskSeverity | Mercantile    | 0075 Medium | Added |
| OccupCategoryRiskSeverity | Mercantile    | 0076 Medium | Added |
OccupCategoryRiskSeverity Motels and Hotels 0074 Not Applicable Added
OccupCategoryRiskSeverity Motels and Hotels 0075 Not Applicable Added
OccupCategoryRiskSeverity Motels and Hotels 0076 Not Applicable Added
| OccupCategoryRiskSeverity | Offices | 0074 Not Applicable | Added |
| ------------------------- | ------- | ------------------- | ----- |
| OccupCategoryRiskSeverity | Offices | 0075 Not Applicable | Added |
| OccupCategoryRiskSeverity | Offices | 0076 Not Applicable | Added |
OccupCategoryRiskSeverity Residential Apartments and Condominiums 0074 Not Applicable Added
OccupCategoryRiskSeverity Residential Apartments and Condominiums 0075 Not Applicable Added
OccupCategoryRiskSeverity Residential Apartments and Condominiums 0076 Not Applicable Added
| OccupCategoryRiskSeverity | Service | 0074 Low | Added   |
| ------------------------- | ------- | -------- | ------- |
| OccupCategoryRiskSeverity | Service | 0075 Low | Added   |
| OccupCategoryRiskSeverity | Service | 0076 Low | Added   |

Rate Tables Tabs

The Rate Tables reports -- Rate Tables, Rate Table Keys, Rate Table Value Column,
and Rate Table Entries -- contain all the information used to compute a rate, loss cost,
factor or a stat code.

Rate Tables Tab

The Rate Tables tab contains two or more columns, one or more key columns, and a
value column.  See the example below.

37  ISO ERCTM Suite Product Guide

In this example, the key column is named ConstructionTypeToUse and the value
column is named Rate. To compute the rate, a particular construction is looked up in the
ConstructionTypeToUse column and then the matching rate value is pulled from the
BroadFormBaseRate that is to be computed.
Rate Table Keys
Rate Table Keys determine the appropriate match for a loss cost lookup called from an
algorithm. Keys must begin with a letter and may include letters, numbers, or currency
symbols. A rate table is required to have at least one key. Generally, keys are matched
values from a domain table.
As described in the Domain Table tab section, these entries are very important in
relation to our rate tables. Our rate table lookup always passes a parameter; the value
in most cases is obtained from a field that uses a domain table. The lookup method of a
rate table uses the data value that is passed by the domain table through the page field
to return the correct value from the table.
The Rate Table Key must have a valid data type. The following are valid data types:
• Date - The key field has a date value. When the date data type is specified, the size
and scale fields are not used.
• Decimal - The key field has a decimal value. When the decimal data type is
specified, the size value must be specified, and the scale value may be specifically
optionally.
• Integer - The key field has an integer value. When the integer data type is
specified, the size and scale fields are not used. The integer data type will store a
value between -2,147,483,648 and 2,147,483,647.
• Long - The key field has a long value. When the long data type is specified, the size
and scale fields are not used. The long data type will store a value between -
9,223,372,036,854,775,808 and 9,223,372,036,854,775,807.
• Text - The key field has a text value. When the text data type is specified, the size
value must be specified.
Note: When a domain table is specified as a key in a rate table, the domain table name
is the same as the name of the rate table key. In general, when a rate table key is a
domain table, the data type of the key and the domain table must be the same.
However, when creating a rate table key that is a domain table with a range type, the
38 ISO ERCTM Suite Product Guide

rate table key must have a data type of text, regardless of the data type of the domain
table.
Rate Table Value Columns Tab
Rate Table Entry Column values also require a data type. The column value field has a
name such as factor. The value name must begin with a letter and may include letters,
numbers, or currency symbols. The following are the possible data types for the value
field:
• Date - The field contains a date value. When the date data type is specified, the
size and scale fields are not used.
• Decimal - The field contains a decimal value. When the decimal data type is
specified, the size value must be specified, and the scale value may be specified on
an optional basis. If optional, then the scale of the data value may be set if the type
is set to decimal.
• Integer - The field contains an integer value. When the integer data type is
specified, the size and scale fields are not used. The integer data type stores a
value between -2,147,483,648 and 2,147,483,647.
• Long - The field contains a long value. When the long data type is specified, the
size and scale fields are not used. The long data type stores a value between -
9,223,372,036,854,775,808 and 9,223,372,036,854,775,807.
• Text - The field contains a text value. When the text data type is specified, the size
value must also be specified.
• Size - The length of the data value is specified in the size field if the type is set to
decimal or text.
39 ISO ERCTM Suite Product Guide

The result of a rate table lookup value is placed in a column determined by the structure
of the line of business. This column is then called in a specific order of operation within
a coverage algorithm.
Process Example:
Algorithm
Domain
Table
Assignment
Table Key
Column
Page Field
Rate Table
Value
Following is an example of the process used with rate tables using Rule 41.D, Collapse
During Construction, as an illustration. We can see that the Collapse options available
to select are Options 1, 2, and 3. The rate is looked up from the
BldrsRiskCollapseDuringConstrctnRate rate table. Following the algorithm, you will see
that the rate determined will then be subtracted by 1 before being multiplied by the
Broad Rate on the Commercial Property Structure table.
40 ISO ERCTM Suite Product Guide

41 ISO ERCTM Suite Product Guide

Rate Table Entries
Rate table entries are derived by look-up methods. This involves placing the
appropriate matched value from the rate table entries to the designated column on a
line of business table. The following are valid lookup types:
• Exact Match - The key field has a lookup type of Exact Match. When Exact Match
is specified, a particular value is looked up in the key column and the matching value
is added to the rate that is to be computed.
• Less Than - The key field has a lookup type of Less Than. When Less Than is
specified, a particular value is looked up in the key column and matched with the row
containing the highest value that is less than the value being looked up.
• Less than or Equal - The key field has a lookup type of Less than or Equal. When
Less than or Equal is specified, a particular value is looked up in the key column and
then matched with the row containing the highest value that is less than or equal to
the value being looked up.
• Greater Than - The key field has a lookup type of Greater Than. When Greater
Than is specified, a particular value is looked up in the key column and matched with
the row containing the lowest value that is greater than or the value being looked up.
• Greater Than or Equal - The key field has a lookup type of Greater than or Equal.
When Greater than or Equal is specified, a particular value is looked up in the key
column and matched with the row containing the lowest value that is greater than or
equal to the value being looked up.
• Interpolate - The key field has a lookup type of Interpolate. When Interpolate is
specified, a particular value is looked up in the key column and then the matching
value is added to the rate that is to be computed. In the event that the value falls
between two entries in the rate table the return value is determined by interpolating
between the two rates in the table.
Key Factor
0 1.84
1 5.51
4 11.40
9 29.41
42 ISO ERCTM Suite Product Guide

| Lookup   |     |           |  If key = 3 ( 3 is the value being  |          |
| -------- | --- | --------- | ----------------------------------- | -------- |
| Type     |     | Strategy  |                                     | passed)  |
Exact  The rate table key field value  Error - Lookup will fail.
| Match  | must exactly match the value  |     |     |     |
| ------ | ----------------------------- | --- | --- | --- |
being passed into the rate
table from the rate request.
Less Than  The system checks if the  is value of 3 less than 0 - No
|     | value being passed is less  |     | is value of 3 less than 1 - No  |     |
| --- | --------------------------- | --- | ------------------------------- | --- |
than the lowest value in the  is value of 3 less than 4 - Yes,
|     | table and then works its way  |     | return 11.4  |     |
| --- | ----------------------------- | --- | ------------ | --- |
up to compare against the
next highest value in the table.
Less Than  The system checks if the  is value of 3 less than or equal to 0
| or Equal  | value being passed is less  |     | - No  |     |
| --------- | --------------------------- | --- | ----- | --- |
than or equal to the lowest  is value of 3 less than or equal to 1
|     | value in the table and then  |     | - No  |     |
| --- | ---------------------------- | --- | ----- | --- |
works its way up to check  is value of 3 less than or equal to 4
|     | against the next highest value  |     | - Yes, return 11.4  |     |
| --- | ------------------------------- | --- | ------------------- | --- |
in the table.
Greater  The system checks if the  is value of 3 greater than 9 - No
Than  value being passed is greater  is value of 3 greater than 4 - No
than the highest value in the  is value of 3 greater than 1 - Yes,
|     | table and then works its way  |     | returns 5.51  |     |
| --- | ----------------------------- | --- | ------------- | --- |
down to check again the next
lowest value in the table.
Greater  The system checks if the  is value of 3 greater than or equal
| Than or  | value being passed is greater  |     | to 9 - No  |     |
| -------- | ------------------------------ | --- | ---------- | --- |
Equal  than or equal to the highest  is value of 3 greater than or equal
|     | value in the table and then  |     | to 4 - No  |     |
| --- | ---------------------------- | --- | ---------- | --- |
works its way down to check  is value of 3 greater than or equal
|     | again the next lowest value in  |     | to 1 - Yes, returns 5.51  |     |
| --- | ------------------------------- | --- | ------------------------- | --- |
the table.
Interpolate  The system performs linear  ((3 - 1)* (11.40 - 5.51)/(4 - 1)) +
|     | interpolation.   |     | 5.51  |     |
| --- | ---------------- | --- | ----- | --- |
= (2 x 5.89 / 3) + 5.51
= 9.44  (rounded to 2 decimals in
this example)

| 43  ISO ERCTM Suite Product Guide  |     |     |     |     |
| ---------------------------------- | --- | --- | --- | --- |

Page Tabs
The Page tabs – Page, Page Fields, and Page Related Fields -- represent what is
displayed on a screen when a page is loaded into a rating system. For example, what
fields are on a page, and what are the size and type of those fields.
Page Tab
A page has three main types and can be associated with a policy, risk, or a form. Each
page is associated with a table; this table links the rating content to the algorithms.
Every page can only be associated with a single table. As a result, this relationship
between pages and tables contains the hierarchy structure for the state rating content.
For a given line of business, there is one policy page. As a child of this policy page,
there can be either risk or form pages. To identify what tables are risks versus forms,
apply a filter so only the Policy or Policy Detail columns are displayed. Once this filter is
applied, go to the “Type” column and select “Summary”; the result will provide a list of
44 ISO ERCTM Suite Product Guide

all child risks of the policy. If the parent was changed as a result of the first filter, the
result is the second tier of risk pages within the state content. This process can
continue until all risk pages are determined. The final product is a wireframe guide for
the state. This same process may be executed for forms; the only difference is under
the filter criteria would be “Form“ not “Summary”. The majority of pages within the
rating content are forms.
Below is a sample hierarchy for pages.
Policy
Forms
Risk Risk
Risk Forms Risk Forms
Forms Forms
Below is an example of the Page tab followed by a description of the information it
provides:
45 ISO ERCTM Suite Product Guide

• Name - Represents the name of the page. If a page is a form page, the name is the
name of the form.
• Parent - Lists the name of the parent page. The parent of a policy page is blank.
• Table - This is the name of the table that is associated with the page.
• Type - There are three types of pages:
1. Form - The page is a form page, representing a form in the ISO Manual.
2. Detail:
a. Policy Detail Page - Each line of business has one policy page. Policy page
is the type detail and is always the first page in sequence.
b. Risk Level Detail Page - Each risk level can have a risk page. Risk page is
the type detail.
c. Form Detail Page – The form detail page represents schedule of a
corresponding form. It is used to capture data for that form.
3. Summary - Summary pages are used to summarize the key fields of a detail
page. Summary pages can be ignored.
• Form Type - If a page is a form page, there are three types of form pages:
1. Mandatory Forms – Must be applied to a policy.
2. Conditional Forms – Must be applied to a policy if a condition is met. (The
condition can be found in the Algorithms under Form Attachment Logic.)
3. Optional Forms – Overall, optional forms do not have a condition for an
attachment, therefore the condition column is blank. However, if an optional form
has a condition, then the condition is being used to determine whether or not the
form can be used in the policy (eligibility).
Note: mandatory and conditional forms are found in the ISO CLM as mandatory.
Optional forms are found in the ISO CLM as optional.
• Number - If the page is a form page, then the form number will be specified. For
example, for form CP 00 90 07 88, “CP 00 90” is the form number and “07 88” is the
edition date. If the page is a form page and no form number is provided, then this
means the page was created for data collection purposes.
46 ISO ERCTM Suite Product Guide

• Min Occurs/Max Occurs - Indicates the minimum and maximum number of iteration
of form availability on a policy:
o Mandatory Forms - Min Occurs = 1, Max Occurs = 1
o Conditional Forms - Min Occurs = 0, Max Occurs = 0 Note: conditional forms
depend on certain scenarios or conditions in order to apply to a policy. When a
policy is created, the conditional form attachment logic is based on certain user
selections. Therefore, the default for min/max is “0/0” because a form can’t be
added by a user unless it is determined whether or not a condition is met.
o Optional Forms - Min Occurs = 0, Max Occurs > 99
• Hide Premium - This Yes/No indicator identifies whether the form page is premium
bearing. Yes means it is not premium bearing; no means it is premium bearing.
• Condition - This is the condition for "Optional" forms to be available for selection.
• Variable – This identifies forms that have variable versus static data.
• Scheduled – Identifies schedule forms.
The following list of information is only used with the ERC+software product. As of October
2018, this information is being removed from ERC. If you are working with ERC
releases prior to this time, please disregard this information.
1. Sequence
2. Sub Sequence
3. Comment
4. Before Script
5. After Script
6. Template File
7. Tab Condition
8. Tab Resource Name
9. BtnResAdd
10. BtnCndAdd
11. BtnLblAdd
12. BtnResModify
13. BtnCndModify
14. BtnLblModify
15. BtnResDelete
16. BtnCndDelete
17. BtnLblDelete
18. BtnResViewDetail
19. BtnCndViewDetail
20. BtnLblViewDetail
21. BtnResCopy
47 ISO ERCTM Suite Product Guide

22. BtnCndCopy
23. BtnLblCopy
24. BtnResRenumber
25. BtnCndRenumber
26. BtnLblRenumber
27. BtnResView
28. BtnCndView
29. BtnLblView
Illustration of ISO Form with Detail Pages
If a form needs to capture additional information for multiple occurrences, a detail page
can be added. For example: Outdoor Signs (CP 14 40):
Page Outdoor Signs is a form page. Outdoor Signs Detail page is used to capture the
schedule on form CP 14 40 shown on the ISO form.
Color Codes
48 ISO ERCTM Suite Product Guide

The use of color coding represents the status of the content, whether a page has been
added, changed, or deleted from the content compared to the inherited base or parent
content:
• Black - Indicates the content is inherited from the parent content.
• Blue - Indicates the content is added or modified from the parent content.
• Red - Indicates the content is deleted from the parent content.
How to Use Pages to Generate a Hierarchy or List of Forms for Certain
Criteria
The Rating Content pages can be used to create a line of business hierarchy or a list of
all the forms available in a policy level. See the steps below followed by an illustration.
Page Hierarchy for Commercial Property:
1. Within the Rating Content file, start from the "Policy Detail" page and work down.
2. Filter type by "Summary", and then select parent "Policy Detail" to identify the policy
level risks. Ignore "Payment" page.
3. Repeat the same steps to identify the risks under each of the policy risk levels.
Policy Forms
Location Forms
Building F Special Form
o Class s
r
Occupan Business m Special Class Forms
cy Class Income s Business Income
Personal Forms Forms
Property
List of forms available in a policy level:
1. Filter type by "Form", and then filter "Parent" by a particular risk level.
2. Conditions can be specified for optional forms. To generate a list of forms for certain
criteria, use the conditional filter to obtain a list.
49 ISO ERCTM Suite Product Guide

Page Fields Tab
Page Fields are used to capture the information or data required to rate policies. The
data captured through the page fields can also be used to determine the form
attachment logic. Page fields are always tied to columns. Just as columns are a subset
of tables, page fields are a subset of pages. See the example below followed by a brief
description of the columns.
• Page - The name of the page on which the page field is displayed.
• Field - The name of the page field. The Page field name is the same as the column
name.
• Sequence - Determines the order in which the Page fields are displayed on the
page.
• Type - Controls how data should be entered into the page field -- input data fields
versus read-only fields. Page fields can be any of the below type:
50 ISO ERCTM Suite Product Guide

o Anchor – A hyperlink that the user clicks to invoke a local file, such as an HTML,
PDF, or image file. Fields of this type can be ignored.
o Button - A search button that the user clicks to perform a search for a client
name or address. When using buttons they must be applied to Unique Identifiers
that are linked to the Address, Company, or Human table.
o Checkbox - A check box where an item can be selected to indicate Yes/No or
1/0
o Dialog - A text box and a select button were used. When a user clicks the select
button, the system displays an external web page in a web page dialog box. The
user can specify the file name of the external web page in the dialog file name
field and the type of the file (either HTML or XSL) in the dialog file type field.
o Hidden – Is used for system purposes mostly to store information captured at a
different risk or policy level which is not required to be displayed. Fields of this
type can be ignored.
o Radio – Is used to select an item. Radio buttons appear in a horizontal format,
and a domain table must be associated with the radio page field type. This is
mostly used for Yes/No selections.
o Radio - Vertical – Is used to select an item. The radio buttons appear in a vertical
format, and a domain table must be associated with the radio page field type.
o Select - A drop-down list of items from which the user selects one item. A
domain table must be associated with the select page field type.
o Text - A text field that can accommodate a single line of user-entered text. Note:
Data entered in page fields of this type is controlled by the type of column tied to
the page field, for example a page field tied to an integer column cannot have
string being entered.
o Text Area - A text area can accommodate multiple lines of user-entered text.
Text areas are associated with columns of type Text.
• Label - Displays the page field label as it will appear in the web page in the user
interface.
• Text Area Rows - Specifies the number of rows for a text area page field.
• Text Area Columns - Specifies the number of columns for a text area page field.
• Quote Read Only - This is a Yes/No indicator that specifies that the page field
cannot be edited on a quote page. For example, page fields to display premium,
rates and factors output from the system.
• Quote Required - This is a Yes/No indicator that specifies that the entry is required
for the Page Field on a quote page.
• Quote Display - This is a Yes/No indicator that specifies that the Page field is
displayed on a quote page.
51 ISO ERCTM Suite Product Guide

• Policy Read Only - This is a Yes/No indicator that specifies that the Page field
cannot be edited on a policy page. For example, Page fields to display Premium,
Rates and Factors which should not be modified.
• Policy Required - This is a Yes/No indicator that specifies that the entry is required
on a policy page.
• Policy Display - This is a Yes/No indicator that specifies that the Page field is
displayed on a policy page.
Note: Different controls exist for quote and policy. If you are working with both quote
and policy, these fields may be of value, otherwise ignore them.
Most fields required for premium determination are quote and policy required, however,
certain fields used for data capture and statistical assignment purposes may only be
policy required. The Occupancy Description, Name and Address fields illustrated in the
above example are policy required and not quote required.
• Default - Allows the user to enter a default value for the page field. It is also used
with anchor type page fields to store the path location for desired document.
• Min - This controls the minimum value for a page field.
• Max - This controls the maximum value for a page field.
• Domain Table - This specifies a domain table that is associated with the page field.
The type of fields eligible for domains are radio, radio-vertical, select, and text.
Field Sequence Type Label Default Domain Table
Type of
Burglar Alarm Not
BurglaryAlarmSystemType 400 Select System Applicable BurglaryAlarmSystemType
Domain tables can be associated with a page field to capture information, if there is a
list of options. As shown above the “BurglaryAlarmSystemType” domain table is
associated with the BurglaryAlarmSystemType page field.
The domain table contains a list of Burglar alarm system types. The Default Parameter
contains the default value of the page field if no selection is made.
52 ISO ERCTM Suite Product Guide

• Help - This allows for the entry of help text to be displayed when the mouse is
placed over the page field. This column is for internal purpose and can be ignored.
• Help Text - Provides for entry of detailed help text that is displayed when the page
field label is clicked. This text is more detailed than the text entered in the “Help”
parameter and may exceed 128 characters. This column is for internal purposes and
can be ignored.
• Condition - This is the condition based on which the page field is displayed.
• Required Condition - This is the condition that makes the page field required.
Field Condition Required Condition
BurglaryAlarmSystemType != "Not BurglaryAlarmSystemType != "Not
BurglaryAlarmCreditFactor Applicable" Applicable"
The Condition parameter specifies the condition for the “BurglaryAlarmCreditFactor”
page field to appear in the user interface.
Rating Rating Required
Table Column
Required Condition
CommercialPropertyBurglaryAndRobbery BurglaryAlarmSystemType
ProtectiveSafeguards BurglaryAlarmCreditFactor Yes != "Not Applicable"
The Required Condition parameter specifies the condition for the
“BurglaryAlarmCreditFactor” page field to be used as a required input for rating.
The column to which the page field is tied also has the rating required condition. This
rating required condition can be referenced in the “Ratebook Columns” tab in the ERC
file.
• Display Controller - This specifies whether the page field controls the display of
other page fields on the page. This column is for internal purposes and can be
ignored.
• Print Required – Identifies variable data fields on the ISO forms that may be
required for print. 0 = N or No; 1 = Y or Yes.
The following list of information is only used with the ERC+software product. As of October
2018, this information is being removed from ERC. If you are working with ERC
releases prior to this time, please disregard this information.
1. Text Display Size
2. Quote Disabled
3. Policy Disabled
4. Mask, Link Text
53 ISO ERCTM Suite Product Guide

5. View Resource
6. Modify Resource
7. Comment
8. Script Before
9. Script After
10. Script Change
11. Amendable Post Issuance
12. Amendable Pre-Renewal
13. XslValue
14. DialogFileName
15. DialogFileType
16. Reference Table
17. LOB Tab Name
18. LOB Tab Sequence
19. LOB Tab Coverage Part
20. Display Mode
21. Display Mode Condition
22. Display Mode Read Only
23. ESI Template File Name
24. ESI Labels Defined In Template
Use of Page Fields
A page field can be data collect or data display. To capture all data collect fields, filter
"Quote Required" or "Policy Required" fields by "Yes" and also ignore all read-only
fields.
How to Identify Coverages
To identify coverages for a line of business, identify the page fields with the format
Table.Column.
For example:
CommercialPropertyPersonalPropertyPrsnlPropCoverage.PolicyTermPremium, this
identifies coverage CommercialPropertyPersonalPropertyPrsnlPropCoverage.
How to Identify Data Capturing Fields for a Form
To identify data capturing fields on a form, select the page name of the form and
generate the fields on the form page or detail page.
54 ISO ERCTM Suite Product Guide

Page Related Fields Tab
The purpose of the Page Related Fields tab is to identify the controlling elements for a
particular domain table. This will structure any page field that has a domain table
associated with it. If a domain table has a key or pre-requisite values associated with it,
the controlling elements need to be aligned with it.
The way to read the information in this tab is as follows:
• Page – This column identifies the page where the page field resides (e.g., Policy
Detail).
• Field - Provides the name of the page field that has a domain table associated with
it.
• Domain Table – Identifies the name of the domain table associated with that field.
• Related Field and Related XPath - Are mutually exclusive; you can’t have values in
both.
55 ISO ERCTM Suite Product Guide

Algorithm (ALG) Files
The Algorithm files in ERC outline business rules from the ISO CLM for a particular line
of business that are in effect at a certain point in time, including but not limited to
business rules for:
• Form attachment logic for endorsements/forms
• Statistical code assignment logic
• Rating messages
• Premium development and rating procedures
Structure of Algorithm (MS Excel version)
There are many worksheets or tabs in an algorithm (ALG) file, the number of which vary
by line of business. However, all ALG files start with a Table of Contents and
Application tab and end with a Flowchart tab; in between are separate tabs for each
algorithm. See a summary of ALG tabs below.
• Table of Contents - Provides a list of, and links to, all the algorithms contained in
the ALG file. See example below followed by a brief description of each column.
o Algorithm - Lists the worksheet pages in the order that they appear in the ALG
file.
56 ISO ERCTM Suite Product Guide

o Rule Reference - Identifies the ISO CLM rule number associated with the
calculation. If a rule does not apply, then other descriptive information is
provided.
o State Indicator - Indicates whether the primary calculation header (PCH) within
the ALG is countrywide (CW) or state specific (e.g., AK).
• Application Version – Identifies the version and date of the parser used to
generate the ALG.
• Error Messages – Provides the logic for all validation messages.
• Stat Assignment Info – Provides the logic for all statistical code assignment.
• Form Logic – Provides the logic for form attachment logic.
• Common Rating or Risk Common Rating - Contains common rating elements for
either the policy or for a given risk.
• Total Policy Premium or Total Risk Premium - Outlines the accumulation of
premiums for all child coverages, forms, and risk for a given level
• Coverage on Policy Indicator - Contains the conditions under which a coverage is
included on a policy.
• Flowchart – Outlines in a tree structure the exact order of processes that should be
followed in order to calculate a premium correctly.
The following are available for each risk, coverage or form that is premium bearing.
• Table Objects - Provides a list of all Table nodes.
o Illustrates a hierarchy review.
o Illustrates which level (State or CW) the table applies to.
• Column Nodes – Provides a list of all Columns nodes. Each is identified as “Used”
or/and “Used P”.
o Used – Column Node is used in Rating but not in a Premium Calculation on that
table.
o Used P – Column Node is used in Rating and in the Premium Calculation on that
table.
To determine all column definitions for those active values, a compiled list can be
created using this tab. Once compiled, this list can be used as a cross reference
with the DS file under “Column Details” to pull out the exact definition of each
object/column, including type and size.
Algorithm Body and Operations
Below is an example of an algorithm followed by a description of its contents.
57 ISO ERCTM Suite Product Guide

• Primary Rule – Identifies the rule number from the ISO CLM and the name of the
table object.
• DB Tables Used – Identifies the name of the database table used.
• Calculation headers are highlighted in purple indicating a box of logic for the
assignment. The box of logic includes assignments and conditions. The premium
calculation is first established and the logic then works its way down to get each
individual rate and factor.
• Column A – Is used to facilitate machine readability. See acronym definitions
below:
Acronym Description
BBB Begin Block Build
BOF Beginning of File
CCH Class Calculation Header
COM Comment
CVE Calculation End
CVM Calculation Body
CVS Calculation Start
EIF End IF
58 ISO ERCTM Suite Product Guide

ELS Else
EOF End of File
FRS FOR LOOP Start
IFB IF Begin
IFE IF End
IFM IF Body
PCH Premium Calculation Header
RUL Rule Information
SCH Set node Calculation Header code
TAB DB Table used
• Column B – Provides an indicator that defines code as either CW or State. See
acronym definitions below:
Acronym Description
CW1/CW2 CountryWide
SRC Source
ST1 State
• Column C - Defines the three types of logic used in an algorithm:
1. Assignment – Identifies the start of the assignment name
2. Condition – Identify if/else statements
3. Looping - Indicates a looping function
• Column D – Provides the types of Operators. The list of operators includes but is
not limited to the following:
o Numerical Operands: - =, +, -, *, /
o Logical Operands: Or, And, Is Equal To
o IF/ELSE
o Rounding
• Column E - Defines the variables
• Column F - Defines the variable Type
59 ISO ERCTM Suite Product Guide

Acronym   Description
| COLUMN_NUMERIC  |     | Class Column Nodes               |     |
| --------------- | --- | -------------------------------- | --- |
| COLUMN_STRING   |     | Class Column Nodes - String      |     |
| CONSTANT        |     | Constant                         |     |
| LV_BOOLEAN      |     |  Local Variable of type boolean  |     |
| LV_DATE         |     |  Local Variable of type date     |     |
| LV_DOUBLE       |     |  Local Variable of type double   |     |
| LV_INTEGER      |     |  Local Variable of type integer  |     |
| LV_STRING       |     |  Local Variable of type string   |     |
Local Variable that stores the difference between
LV_TimeSpan  dates in an integer format.  This difference can
be Days, Months, or Years
| RT             |     | Rate Table                          |     |
| -------------- | --- | ----------------------------------- | --- |
| UI             |     | User Input Field                    |     |
| XPATH          |     | Other Class Column Nodes            |     |
| XPATH_NUMERIC  |     | Other Class Column Nodes - Numeric  |     |
| XPATH_STRING   |     | Other Class Column Nodes – String   |     |

•  Column G - Defines the end of logic

The following table contains a list of XML elements including their attributes and a
parent/child relationship:

|     | Element  | Attributes  | Possible Child  |
| --- | -------- | ----------- | --------------- |
Elements
| Arg  |     | number  |     |
| ---- | --- | ------- | --- |
variableType
| assign  |     | state  | expression  |
| ------- | --- | ------ | ----------- |
recordType
lValue
variableType
| ATTACH  |     | state  |     |
| ------- | --- | ------ | --- |
recordType
form
| bracket  |     | expression  |         |
| -------- | --- | ----------- | ------- |
| class    |     | name        | class   |
|          |     | type        | rating  |
|          |     | pass        | stat    |
err
formAttachment
premium
| 60  | ISO ERCTM Suite Product Guide  |     |     |
| --- | ------------------------------ | --- | --- |

| ColumnNode  | usage       |             |
| ----------- | ----------- | ----------- |
| condition   | state       | expression  |
|             | recordType  |             |
| Else        | state       | if          |
|             | recordType  | else        |
|             | excelSheet  | assign      |
|             | excelRow    | loop        |
| Err         | className   |             |
variables
type
| expression  | side           | expression  |
| ----------- | -------------- | ----------- |
|             | ruleReference  | function    |
|             | recordType     | ratetable   |
|             | Op             | bracket     |
asText
variableType
| formAttachment  | className  |     |
| --------------- | ---------- | --- |
variables
type
| function  | Type         | arg         |
| --------- | ------------ | ----------- |
| if        | state        | condition   |
|           | recordType   | then        |
|           | excel Sheet  | else        |
|           | excel Row    | ATTACH      |
OptOutForm
| LOB  | name  | reference  |
| ---- | ----- | ---------- |
RatebookId
Version
ParentName
AssemblyId
| loop        | through     | if       |
| ----------- | ----------- | -------- |
|             | state       | loop     |
|             | recordType  | assign   |
| OptOutForm  | OptOut      |          |
Key
FormNumber
FormName
| PCH  | state       | if       |
| ---- | ----------- | -------- |
|      | number      | then     |
|      | name        | else     |
|      | recordType  | assign   |
|      | excelSheet  | loop     |
|      | excel Row   | class    |
|      | overridden  | ATTACH   |
OptOutForm
61  ISO ERCTM Suite Product Guide

| Premium  | className  |     |
| -------- | ---------- | --- |
variables
type
pass
| ratetable  | code       | arg  |
| ---------- | ---------- | ---- |
| Rating     | className  |      |
variables
type
pass
| reference  | number  | class      |
| ---------- | ------- | ---------- |
|            | name    | scope      |
|            | Type    | TableName  |
dbTables
state
inherited
| scope  | ruleReference  | if       |
| ------ | -------------- | -------- |
|        | recordType     | PCH      |
|        | dbTables       | assign   |
|        | pass           | loop     |
|        | state          | class    |
|        | inherited      | ATTACH   |
| Stat   | className      |          |
variables
type
| TableName  | name           | ColumnNode   |
| ---------- | -------------- | ------------ |
|            | ruleReference  | TableName    |
multipleAllowed
hasPremium
foundInLayer
| then  |     | assign   |
| ----- | --- | -------- |
if
loop
ATTACH
OptOutForm

The following table provides the purpose of each element within the XML.

Element  Purpose
arg  Defines the values that are being used within either a rate
table look up or a count function
assign  Defines the process when a value is being set
ATTACH  Associated with conditional mandatory logic and is used to
illustrate the process of attaching a form
Bracket  Used to demonstrate order of operations within the code
62  ISO ERCTM Suite Product Guide

class These are tied to the execution flow reference type and are
used to identify the table being called in the order of operations
for the ALG
ColumnNode Defines every column on a table (same as in the DS file) and
determines if it is used within the rating process
condition The condition element is a child of an if node and is the
starting point of the body of the condition
Else If the condition for an If statement is false this else contains the
catch
Err Tells which error message PCH’s should be rated within the
Err-table name reference
expression An expression defines logic within the ALG, whether it is a
comparison or an assignment
formAttachment Tells which form attachment PCH’s should be rated within the
form-table name reference
function Only available function is a count where tally logic is applied.
The arg listed would be the table being tallied up
if Starts the section of XML tied to a condition within the logic
LOB Starting Element of the XML structure. Identifies the Line Of
Business, Ratebook ID and the Version number of the parser
used to create the ALG
loop Defines the process of looping through the Line of Business
hierarchy. The path is provided in the through attribute and
the starting point is the scope of the reference
OptOutForm Tied to General Liability Opt out Functionality
PCH Defines either a column node or a table that is being set within
the proceeding XML
Premium Tells when a table should generate Premium and what the
associated PCH's associated with that calculation
ratetable Defines the call to do a rate table lookup using the Args
provided as the criteria elements
Rating Tells which PCH’s should be rated within the reference for the
tables pass in the ALG Flow Chart
reference Contains the section name of the ALG. The name is tied to
the tab names within the Excel version. The reference also
states the purpose of the section, whether it is an error
message, premium calculation or common rating
scope Defines the table associated with the logic within the reference
Stat Tells which stat assignment PCH’s should be rated within the
Stat Assignment reference
63 ISO ERCTM Suite Product Guide

TableName Defines the tables included within the ALG, provides the Rule
Reference and displays if table is associated with a Premium
Calculation
Then Then elements are associated with If elements and contain the
action when the condition is true
The following table provides the purpose of each attribute within the XML:
Attribute Purpose
AssemblyId This stores a GUID that will allow a connection between the
ALG and the Id value stored in the RC XML
asText Give a definition of what the intention is of the following section
of XML, this is for documentation purposes only and does not
impact the rating process
className Contains the name of the table where logic is being applied
code Contains the name of the Rate Table being used in the Rating
Process
dbTables Defines the table used within a reference
excelRow Documents the row number within the excel version that
contains the logic for the following section of XML. This is
used for documentation only and does not impact the rating
process
excelSheet
Documents the sheet tab within the excel version that contains
the logic for the following section of XML. This is used for
documentation only and does not impact the rating process
form Defines the table being attached within an attach element
FormName Used for Opt Out functionality within GL
FormNumber Used for Opt Out functionality within GL
foundInLayer Defines where table is found within the different hierarchy
layers
hasPremium Defines if a table has a premium calculation
Inherited This is an attribute on references that shows is logic is
deviated from CW or not
Key Used for Opt Out functionality within GL
lValue Assignment logic where value is being assigned is on the left
side of the equation
multipleAllowed Defines if a table is allowed multiple occurrences or not, if so
the RC file gives the maximum value
64 ISO ERCTM Suite Product Guide

name Defines the name of the object for a PCH element
number Defines order to the element Arg
Op Defines the operator for an expression
OptOut Used for Opt Out functionality within GL
Overridden Shows where value is inherited from CW or deviated within the
state. It also shows if state specific logic is unique to the state
or a deviation from CW
ParentName With the state file it gives the name of the CW the ALG inherits
from
pass Gives an order when references are called multiple times, pass
references to the order call for references
RatebookId Defines the name of the ALG
Rating Defines variables for class files that are used in rating the ALG
but are not directly tied to a premium calculation
recordType Contains the acronym for machine automation purposes on
what the element is used for in the ALG
ruleReference Defines what rule the table is associated with
side Defines which side of an express the value applies
state Denotes whether content is CW versus State specific
through Defines the X Path logic for a looping statement
Type Defines the type of reference
usage Determines whether column node is used within the ALG or
Not
Variables An attribute of the Rating element, it list which PCH's are to be
rated within that pass in the Flowchart
variableType Gives a definition of what the value is in an expression
Version Defines the version number of the parser used to generate the
ALG
The following table provides a description of the operator values common in every line
of business:
65 ISO ERCTM Suite Product Guide

Operator Value Description
- Subtraction
!= Not Equal To
% "Mod" function
& AND
&& AND
* Multiply
/ Divide
|| OR
+ Addition
< Less than
<= Less than or Equal To
== Equal To (comparison not assignment)
> Greater Than
>= Greater than or Equal To
Increment the year place holder in a date format
AddYears (dd/mm/yyyy)
Converts a decimal to the next whole integer
Ceiling For example, 7.03 becomes 8
DateTime.IsLeapYearEffDat Determines if the time frame provided falls within
e a leap year
Interpolation command that determines rate
Double.ParseLimit rounded to the thousandth
Interpolation command that determines rate
Double.ParselowerDataRow[ rounded to the thousandth, value grabs lower
"Factor" ] factor
Double.ParselowerDataRow[ Interpolation command that determines rate
"Limit" ] rounded to the thousandth, value grabs lower limit
Interpolation command that determines rate
Double.ParseupperDataRow[ rounded to the thousandth, value grabs upper
"Factor" ] factor
Interpolation command that determines rate
Double.ParseupperDataRow[ rounded to the thousandth, value grabs upper
"Limit" ] limit
Used only in General Liability Opt Out Logic and
IndexOf is used to parse an array list
Keyxxxxx.xxFormNumberC Used in General Liability Opt Out tab to store Key
66 ISO ERCTM Suite Product Guide

G xx (class code, xxxxx.xx), Form Number(CG xx
xxFormName../../”Database xx), Form Name (database table and xpath) and
TableName”OptOutBoolean Opt Out Choice (boolean expression) to an
Array List
Used in General Liability Opt Out tab to indicate
KeyoptOutClassCode key within an array list
LeapTest.AddDays1.0 Leap Year Test for Time Range
Math.RoundARDSpan.Days Rounds a Time Span in Days
Node.OwnerDocument.Docu
mentElement.Attributes.GetN Grabs the value of the attribute ratingIteration
amedItem"ratingIteration" from the policy XML
Not Not True
Replace This replaces a value with another
Round Up Dollar Round to the dollar
Round Up Thousands Round to the thousandths
StartsWith StartsWith, this command
Used in data comparison to generate a time range
Subtract by days
A function applied with Replace, Replace a value
With "With" a new value
The following table provides the purpose of the functions that can be applied to values
in the ALG.
67 ISO ERCTM Suite Product Guide

Function Purpose
.Date
Returns the date stored in a local variable
For example
ArdDate.Date
.Days
Applied in conjunction with "TimeSpan" variables and allows dates
to be compared using days as the basis
For example
TimeSpan varaible = date1.Days - date2.Days
.length
Returns the length of the string value, value is an integer
.Month Returns the month portion of a date;
For example
Date - 1/1/2015
Date.Month = 1
.Months
Applied in conjunction with "TimeSpan" variables and allows dates
to be compared using months as the basis
For example
TimeSpan variable = date1.Months - date2.Months
.PadLeft Used with columns or local variables that are strings and allows the
stored value to equal a certain amount of characters
For example
String - 20, if PadLeft is applied with a value of 3
String becomes 020
.Value
Returns the values that are stored in a column
.Year Returns the year portion of a date;
For example
Date - 1/1/2015
Date.Year = 2015
.Years Applied in conjunction with "TimeSpan" variables and allows dates
to be compared using years as the basis
For example
TimeSpan varaible = date1.Years - date2.Years
68 ISO ERCTM Suite Product Guide

The following table provides a description of the types of elements that can be applied
to values in the ALG.
Type Description
Reference element contains rating logic not tied
Common Rating to a premium calculation
Reference element contains underwriting error
Error Messages message logic for the provided dbTable
Reference element contains a order of operation
Execution Flow flow for the ALG
Reference element contains conditional
mandatory logic and mandatory logic for the
Form Logic provided dbTable
Reference element contains the Opt Out logic,
Opt Out only for General Liability
Reference element contains the coverage on
Policy Indicator policy indicator logic for all coverages
Reference element contains a premium
Premium Calculation calculation
Reference element contains the statistical
Stat Reporting assignment logic for all stat codes
Reference element contains the definitions of
Table Objects the table objects and column nodes
The following chart provides a description of the usage types used in the ALG.
Usage Description
Column Node is used in Rating and in the Premium
BOTH
Calculation on that table
Column Node is used in Rating but not in a Premium
OTHERS
Calculation on that table
UNUSED Column Node is not used within the ALG
69 ISO ERCTM Suite Product Guide

Navigation Example
The total Policy Premium tab is a guide which follows the database data structure.
Every risk or form is linked inside a tab to navigate to the corresponding tabs.
Following is the link to the Location Premium tab.
Below is the Building Basic Group I Coverage tab. It first develops the calculation for
premium and then works its way down to develop the rate(s) and factor(s) that are
involved.
70 ISO ERCTM Suite Product Guide

In the first example, it shows that based on the Cov Type, premium = Final Basic Group
Rate x Limit/1000 x IRPM Factors x Multi Premium And Dispersion Credit Factor X
Package Mod Factor.
71 ISO ERCTM Suite Product Guide

Policy Administration Elements
The values listed below will not be found within the rating content for any lines of
business. However, they may be referenced in the algorithm file for some lines. Each
of these values is a sibling of the main line of business table element in the XML
structure for a line of business.
• AnnDate - Anniversary Rating Date for Workers Comp line of business
• EffDate - Effective date of the quote/policy being rated
• ExpDate - Expiration date of the quote/policy being rated
• Renewal - Indicates whether or not the policy is a renewal policy or a first issuance.
• RenewalIteration – Identifies the number of times a policy has been renewed.
• Transaction/Effective – Identifies the date of a modification made to a policy. This
can include creation, issue, or endorsement.
• State/Name - Contains the full name of the State that is being rated.
• State/ID - Contains the unique identifier for that state.
• StateId - Contains the ID of the state associated with the RC.
72 ISO ERCTM Suite Product Guide

Businessowners Hierarchy
CCoovveerraaggeess
BOP
Quote or Policy FFoorrmmss
CCoovveerraaggeess
Location
FFoorrmmss
CCoovveerraaggeess
Building
FFoorrmmss
CCoovveerraaggeess
Classification
FFoorrmmss
73 ISO ERCTM Suite Product Guide

Commercial Automobile Hierarchy
Coverages
CA
Quote or Policy Forms
Coverages Coverages
Trucks Garage Dealers
F orms Forms
C overages
Garage Services
Coverages
Private
Forms Passenger Forms
C overages
Public Vehicles
Forms
Coverages
Special Types
Forms
Coverages
Zone Rated
Forms
74 ISO ERCTM Suite Product Guide

Commercial Inland Marine (Filed) Hierarchy
Inland Marine
Quote or Policy
Coverages
Coverages Signs
Accounts
Receivable Forms
Forms
Coverages
Coverages Theatrical
Camera & Musical Property
Forms
Forms Instruments
Coverages
Coverages Physicians and
Film Surgeons
Forms
Forms
Coverages
Mail
Coverages
Floor Plan
Forms
Forms
Coverages
Valuable Papers
Coverages
Commercial Forms
Articles
Forms
Coverages
Jewelers Block
Coverages Forms
Equipment
Forms Dealers Coverages
Fine Arts
(Texas Only)
Forms
75 ISO ERCTM Suite Product Guide

Commercial Inland Marine (Non-Filed)
Hierarchy

Non-Filed Inland Marine

|     |     |     |     |     | Quote or Policy  |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- |

Annual Transit  Bailees Customers  Builders Risk  Commercial Fine  Computer Systems
|     |     |     |     |     |     |     |     | Arts  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |

| Cov erages  |     |     | Coverages  | Coverages  |     |     | Coverages  |     |     | Coverages  |
| ----------- | --- | --- | ---------- | ---------- | --- | --- | ---------- | --- | --- | ---------- |

| Forms  |     |     | Forms  | Forms  |     |     | Forms  |     |     | Forms  |
| ------ | --- | --- | ------ | ------ | --- | --- | ------ | --- | --- | ------ |

Contractors  Difference in  Exhibition  Fine Arts Dealers  Fine Arts Museums

| Equipment  |     |     | Conditions  |     |     |     | and Galleries  |     |     |     |
| ---------- | --- | --- | ----------- | --- | --- | --- | -------------- | --- | --- | --- |

| Cov erages  |     |     | Coverages  | Coverages  |     |     | Coverages  |     |     | Coverages  |
| ----------- | --- | --- | ---------- | ---------- | --- | --- | ---------- | --- | --- | ---------- |

| Forms  |     |     | Forms  | Forms  |     |     | Forms  |     |     | Forms  |
| ------ | --- | --- | ------ | ------ | --- | --- | ------ | --- | --- | ------ |

Installation  Installment Sales and  Machinery and  Miscellaneous  Motor Truck Cargo
|     |     |     | Leased Property  |     | Equipment  |     |     | Articles  |     |     |
| --- | --- | --- | ---------------- | --- | ---------- | --- | --- | --------- | --- | --- |

| Cov erages  |     |     | Coverages  |     |     |     | Coverages  |     |     | Coverages  |
| ----------- | --- | --- | ---------- | --- | --- | --- | ---------- | --- | --- | ---------- |
Coverages

| Forms  |     |     | Forms  |     | Forms  |     | Forms  |     |     | Forms  |
| ------ | --- | --- | ------ | --- | ------ | --- | ------ | --- | --- | ------ |
Processors  Radio and Television  Railroad Rolling  Riggers Liability  Scientific and Medical
|     |     |     | Towers and  |     | Stock  |     |     |     |     | Diagnostic Equipment  |
| --- | --- | --- | ----------- | --- | ------ | --- | --- | --- | --- | --------------------- |
|     |     |     | Equipment   |     |        |     |     |     |     |                       |

| Coverages  |     |     | Coverages  |     | Coverages  |     | Coverages  |     |     | Coverages  |
| ---------- | --- | --- | ---------- | --- | ---------- | --- | ---------- | --- | --- | ---------- |
| Forms      |     |     | Forms      |     | Forms      |     | Forms      |     |     | Forms      |
Warehouse Operators
|     |     |     | Trip Transit  |     |     |     | Watercraft  |     |     | Yachts  |
| --- | --- | --- | ------------- | --- | --- | --- | ----------- | --- | --- | ------- |
Legal Liability
|     |                                    |            |     |            |     |            |     |     |            |     |
| --- | ---------------------------------- | ---------- | --- | ---------- | --- | ---------- | --- | --- | ---------- | --- |
|     |                                    | Coverages  |     | Coverages  |     | Coverages  |     |     | Coverages  |     |
|     |                                    | Forms      |     | Forms      |     | Forms      |     |     | Forms      |     |
|     | 76  ISO ERCTM Suite Product Guide  |            |     |            |     |            |     |     |            |     |

Commercial Package Policy Hierarchy

CPP
Quote or Policy
| Commercial | General | Commercial |
| ---------- | ------- | ---------- |
Crime Inland Marine
| Auto | Liability | Property |
| ---- | --------- | -------- |
77  ISO ERCTM Suite Product Guide

Commercial Property Hierarchy
Coverages
Commercial Property
Forms
Sche dule Coverages Commercial Property Location
Coverages Forms
Schedule Coverages
Structure Special Class
Coverages Forms
Coverages Forms Special Class
Schedule Business Income
Schedule
Coverages
Occupancy Business Income
Coverages
Coverages
Personal Property
Coverages
Forms
Forms
Schedule Coverages
Coverages
Schedule
Coverages Forms
Forms
Coverages
Schedule
Schedule
Coverages
Coverages
78 ISO ERCTM Suite Product Guide

Commercial Umbrella Hierarchy
Commercial Umbrella
Quote or Policy
Forms Coverages Aircraft BOP Commercial Employers General Garage Liquor Water
Liability Auto Liability Liability Craft
79 ISO ERCTM Suite Product Guide

Crime Hierarchy
Crime
Quote or Policy
Commercial Commercial Employee Theft Government Government Government Kidnap/Ransom
Fidelity Crime & Forgery Fidelity Crime Employee and Extortion
Theft and
Forgery
Coverages Coverages Coverages Coverages Coverages Coverages Coverages
Forms Forms Forms Forms Forms Forms Forms
80 ISO ERCTM Suite Product Guide

Cyber Hierarchy

Cyber                                   Quote or
Policy
| Information  | Financial     | Media And             | Commercial  |
| ------------ | ------------- | --------------------- | ----------- |
| Security     | Institutions  | Information Security  | Cyber       |
| Protection   |               | Protection            |             |
Information
Security Protection
| Coverages  | Coverages  | Coverages  | Coverages  |
| ---------- | ---------- | ---------- | ---------- |
| Forms      |            | Forms      | Forms      |
Forms
81  ISO ERCTM Suite Product Guide

General Liability Hierarchy

Coverages
Schedules
|     | GL               |        |            |
| --- | ---------------- | ------ | ---------- |
|     | Quote or Policy  | Forms  |            |
|     |                  |        | Coverages  |

|     | Location  |        | Schedules  |
| --- | --------- | ------ | ---------- |
|     |           | Forms  |            |

|     | Classification  | Coverages  | Schedules  |
| --- | --------------- | ---------- | ---------- |

Forms
Coverages

| 82  | ISO ERCTM Suite Product Guide  |     |     |
| --- | ------------------------------ | --- | --- |

Workers Compensation Hierarchy
Coverages
Workers Comp
Forms Schedules Coverages
Workers Comp Coverages
Location
Forms Schedules Coverages
Workers Comp Coverages
Classification
Forms Schedules Coverages
83 ISO ERCTM Suite Product Guide