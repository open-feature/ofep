# Open Feature Enhancement Proposals(OFEP)

This repository serves as a focal point for research and experimental work.
It also enables the creation of discussions, proposals and ideation through issues.

We use OFEP: Open Feature Enhancement proposals, which comes from the lineage of [PEP](https://peps.python.org/pep-0001/) much like the Kubernetes project uses [KEP](https://github.com/kubernetes/enhancements/blob/master/keps/README.md) and Open-Telemetry project uses [OTEP](https://github.com/open-telemetry/oteps/blob/main/README.md).

## Is My Thing an enhancement?

We are trying to figure out the exact shape of an enhancement. Until then, here are a few rough heuristics.

An enhancement is anything that:

- a blog post would be written about after its release (eg. [Client-side Feature Flagging](https://openfeature.dev/blog/catering-to-the-client-side))
- requires multiple parties/owners participating to complete (eg. Client-side Feature Flagging [Specification & SDKs])
- will be graduating from one stage to another
- needs significant effort or changes OpenFeature in a significant way (eg. something that would take 10 person-weeks to implement, introduce or redesign a system component, or introduces Specification changes)
- impacts the UX or operation of OpenFeature substantially such that engineers using OpenFeature will need retraining
- users will notice and come to rely on
- impacts multiple implementations or languages

It is unlikely an enhancement if it is:
- rephrasing, grammatical fixes, typos, etc
- bug fixes
- refactoring code
- adding error messages or events
- a thing that affects only a single language or implementation

**Note**: The above lists are intended only as examples and are not meant to be exhaustive. If you don't know whether a change requires an OFEP, please feel free ping someone listed in [sdk-maintainers and cloud-native maintainers](https://github.com/orgs/open-feature/teams) (or) ask in the [CNCF OpenFeature Slack channel](https://cloud-native.slack.com/archives/C0344AANLA1). If you are new, you can create a CNCF Slack account [here](https://slack.cncf.io/).

### OFEP Scope

While OFEPs are intended for "significant" changes, we recommend trying to keep each OFEP's scope as small as makes sense (eg. on broader scale, mentioning the category of the proposal). A general rule of thumb is that if the core functionality proposed could still provide value without a particular piece, then that piece should be removed from the proposal and used instead as an *example* (and, ideally, given its own OFEP!).

## How to start with writing an OFEP? 

- First, [create an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) using the [Enhancement Proposal](https://github.com/open-feature/ofep/issues/new?assignees=beeme1mr&labels=OFEP&projects=&template=Proposal.yaml&title=%5BProposal%5D+) template.
- Fill in the template. Put care into the details: It is important to present convincing motivation, demonstrate an understanding of the design's impact, and honestly assess the drawbacks and potential alternatives.

## Discussing the OFEP

- As soon as the above-mentioned issue is created, potential reviewers (based on the `category of proposal` specified in the issue) would be automatically asked for review. This is done as a preventive measure to avoid long-winded and open-ended discussions in the early design phase of the proposal but the OFEP author should use their discretion here.
- The OFEP author may choose any place for discussions but needs to be linked to the issue. The suggested ones include continuing in the same Github issue or creating a thread on Slack(https://cloud-native.slack.com/archives/C0344AANLA1) mentioning the issue. 
- The OFEP authors are responsible for collecting community feedback on an OFEP before submitting it as a proposal for review. 

## Submitting the OFEP and life-cycle

- Once the idea of the proposal is reviewed by the assigned reviewers, the OFEP author can then reference a Pull Request to the issue containing the proposal. 
- For adding the OFEP as a Pull Request, first, [fork](https://help.github.com/en/articles/fork-a-repo) this [repo](https://github.com/open-feature/ofep).
- Copy [`000-OFEP-template.md`](./000-OFEP-template.md) to `000-OFEP-my-title.md`, where `my-title` is a title relevant to your proposal, and `000` is the OFEP ID. Leave the number as is for now. Once a Pull Request is made, update this ID to match the next smallest available ID.
- Fill in the template and please take care of the details as followed while creating the issue for Enhancement Proposal.
- The initial `status` of an OFEP should be in `drafting` or `pending for review` stage.
- An OFEP is `approved` when atleast two/three reviewers github-approve the PR but this surely depends on its nature. The OFEP is then merged.
- If an OFEP is `rejected` or `withdrawn`, the PR is closed. Note that these OFEPs submissions are still recorded, as Github retains both the discussion and the proposal, even if the branch is later deleted.
- If an OFEP discussion becomes long, or the OFEP then goes through a major revision, the next version of the OFEP can be posted as a new PR, which references the old PR. The old PR is then closed. This makes OFEP review easier to follow and participate in.

## Implementing the OFEP

Some accepted OFEPs represent vital features that need to be implemented right away. Other accepted OFEPs can represent features that can wait until some arbitrary developer feels like doing the work. Every accepted OFEP has an associated issue tracking its implementation in the repository specific to it.

The author of an OFEP is not obligated to implement it. Of course, the OFEP author (like any other developer) is welcome to post an implementation for review after the OFEP has been accepted.
