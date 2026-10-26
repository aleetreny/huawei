"""CareerLab outer loop (policy search) and its equal-budget testbed on SynthCareer.

Generation is emulated by parametric operators on SynthCareer's theta space;
the real lab's generation step is an LLM orchestrator writing policy
revisions (see ``operators``). Allocation, selection and validation run
through ``careerlab.stats`` exactly as they would in the real lab.
"""

from careerlab.search.archive import Node, Outcome, PolicyArchive, descriptors, theta_hash
from careerlab.search.methods import METHODS, SearchConfig, SearchResult, method_config, run_search
from careerlab.search.operators import CandidateStream, Proposal, new_family, recombine, refine, specialize, wild

__all__ = ["METHODS", "CandidateStream", "Node", "Outcome", "PolicyArchive", "Proposal", "SearchConfig",
           "SearchResult", "descriptors", "method_config", "new_family", "recombine", "refine", "run_search",
           "specialize", "theta_hash", "wild"]
