---
date: YYYY-MM-DD
title: OFEP Template
<!--- 
Valid statuses: Approved, Rejected, Withdrawn 
-->
status: Approved
authors: []
tags: []
---

# Name

## State: ( DRAFTING | WITHDRAWN | PENDING REVIEW | APPROVED | REJECTED )

The OFEP begins with a brief overview. This section should be one or two paragraphs that just explains what the goal of this OFEP is going to be, but without diving too deeply into the "why", "why now", "how", etc. Ensure anyone opening the document will form a clear understanding of the OFEP intent from reading this paragraph(s).

## Background

The next section is the "Background" section. This section should be at least two paragraphs and can take up to a whole page in some cases. The guiding goal of the background section is: as a newcomer to this project (new employee, team transfer), can I read the background section and follow any links to get the full context of why this change is necessary? 

If you can't show a random engineer the background section and have them acquire nearly full context on the necessity for the RFC, then the background section is not full enough. To help achieve this, link to prior RFCs, discussions, and more here as necessary to provide context so you don't have to simply repeat yourself.

## Proposal

The next required section is "Proposal" or "Goal". Given the background above, this section proposes a solution. This should be an overview of the "how" for the solution, but for details further sections will be used.

## Sections

From this point onwards, the sections and headers are generally freeform depending on the OFEP. Sections are styled as "Heading 2". Try to organize your information into self-contained sections that answer some critical question, and organize your sections into an order that builds up knowledge necessary (rather than forcing a reader to jump around to gain context).

Sections often are split further into sub-sections styled "Heading 3". These sub-sections just further help to organize data to ease reading and discussion.

### [Example] Implementation

Many OFEPs have an "implementation" section which details how the implementation will work. This section should explain the rough API changes (internal and external), package changes, etc. The goal is to give an idea to reviews about the subsystems that require change and the surface area of those changes. 

This knowledge can result in recommendations for alternate approaches that perhaps are idiomatic to the project or result in less packages touched. Or, it may result in the realization that the proposed solution in this OFEP is too complex given the problem.

For the OFEP author, typing out the implementation in a high-level often serves as "rubber duck debugging" and you can catch a lot of issues or unknown unknowns prior to writing any real code.
