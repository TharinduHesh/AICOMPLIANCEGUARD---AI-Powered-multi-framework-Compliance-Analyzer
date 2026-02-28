"""
Layer 3  ─  GPT / LLM Reasoning Engine
========================================
After the Rule-Based engine (Layer 1) and Semantic engine (Layer 2) identify
gaps, this layer asks a large language model to:

  1. Explain *why* each gap matters (CIA impact).
  2. Suggest concrete improvements.
  3. Rewrite weak clauses professionally.
  4. Return a reasoning-confidence score (0-100).

Falls back to rich rule-based analysis when no LLM is available.
"""

import logging
from typing import Dict, List, Optional

from app.modules.llm_provider import llm_provider

logger = logging.getLogger(__name__)


class ReasoningEngine:
    """
    Layer 3 intelligence wrapper.
    """

    # ── Public API ────────────────────────────────────────────────
    def analyze(
        self,
        structural_results: Dict,
        semantic_results: Dict,
        cia_analysis: Optional[Dict] = None,
        framework: str = "iso27001",
    ) -> Dict:
        """
        Produce reasoning output for a single framework analysis.

        Args:
            structural_results: Output from Layer 1 (rule_engine.analyze)
            semantic_results:   Output from Layer 2 (semantic_engine.analyze)
            cia_analysis:       Optional CIA validator output
            framework:          Framework key

        Returns:
            {
              reasoning_confidence,      # 0-100
              gap_explanations: [...],
              improvement_suggestions: [...],
              rewritten_clauses: [...],
              cia_impact_summary: {...},
              executive_summary: str,
            }
        """
        # Collect gaps from both layers
        structural_missing = [
            s for s in structural_results.get("section_results", [])
            if s["status"] in ("missing", "partial")
        ]
        semantic_weak = [
            m for m in semantic_results.get("clause_matches", [])
            if m["compliance_level"] in ("weak", "partial")
        ]
        missing_controls = semantic_results.get("missing_controls", [])[:10]

        # Build context for LLM
        context = self._build_context(
            structural_missing, semantic_weak, missing_controls,
            structural_results, semantic_results, cia_analysis, framework,
        )

        # Try LLM reasoning
        if llm_provider.is_available:
            return self._llm_reasoning(context, framework)

        # Rule-based fallback
        return self._rule_based_reasoning(
            structural_missing, semantic_weak, missing_controls,
            structural_results, semantic_results, cia_analysis, framework,
        )

    # ── LLM path ──────────────────────────────────────────────────
    def _build_context(
        self, structural_missing, semantic_weak, missing_controls,
        structural_results, semantic_results, cia_analysis, framework,
    ) -> str:
        lines = [f"Framework: {framework.upper()}\n"]

        lines.append("── Structural Gaps (Layer 1) ──")
        if structural_missing:
            for s in structural_missing[:8]:
                lines.append(
                    f"  Clause {s['clause']} – {s['title']} → {s['status']} "
                    f"(keyword coverage {s.get('keyword_coverage', 0)}%)"
                )
        else:
            lines.append("  No structural gaps detected.")

        lines.append("\n── Semantic Weak Matches (Layer 2) ──")
        if semantic_weak:
            for m in semantic_weak[:8]:
                lines.append(
                    f"  \"{m['clause_text']}\" → best match {m['best_control_id']}"
                    f" (sim={m['similarity']:.2f}, {m['compliance_level']})"
                )
        else:
            lines.append("  All clauses have strong semantic matches.")

        lines.append("\n── Missing Controls ──")
        for mc in missing_controls[:8]:
            lines.append(f"  {mc['control_id']}: {mc['title']} [{mc.get('priority','?')}]")

        if cia_analysis:
            cov = cia_analysis.get("cia_coverage", {})
            lines.append(f"\n── CIA Coverage ──")
            lines.append(
                f"  C={cov.get('confidentiality',0):.1f}% "
                f"I={cov.get('integrity',0):.1f}% "
                f"A={cov.get('availability',0):.1f}%"
            )
            lines.append(f"  Balance Index: {cia_analysis.get('cia_balance_index', '?')}")

        lines.append(f"\nStructural Score: {structural_results.get('structural_score', 0)}")
        lines.append(f"Semantic Score:   {semantic_results.get('semantic_score', 0)}")

        return "\n".join(lines)

    def _llm_reasoning(self, context: str, framework: str) -> Dict:
        prompt = (
            "You are an ISO compliance expert. Based on the gap analysis below, provide:\n"
            "1. A concise executive summary (2-3 sentences).\n"
            "2. For each major gap, explain the compliance risk and CIA impact.\n"
            "3. Suggest 3-5 prioritized improvements.\n"
            "4. Rewrite 1-2 weak clauses in professional mandatory language.\n"
            "5. Give a confidence score (0-100) for how well the document meets the framework.\n\n"
            f"=== GAP ANALYSIS ===\n{context}\n"
        )
        try:
            messages = [{"role": "user", "content": prompt}]
            response = llm_provider.generate(messages, max_tokens=1024, temperature=0.3)
            return self._parse_llm_response(response)
        except Exception as e:
            logger.warning(f"LLM reasoning failed: {e}; falling back to rule-based")
            return self._rule_based_from_context(context, framework)

    def _parse_llm_response(self, text: str) -> Dict:
        """Parse structured LLM output into dict. Best-effort."""
        # Extract confidence score if present
        import re
        conf_match = re.search(r'confidence[:\s]*(\d{1,3})', text, re.IGNORECASE)
        confidence = int(conf_match.group(1)) if conf_match else 65

        return {
            "reasoning_confidence": min(confidence, 100),
            "executive_summary": text[:500],
            "gap_explanations": [text],  # Full LLM output as single block
            "improvement_suggestions": [],
            "rewritten_clauses": [],
            "cia_impact_summary": {},
            "source": "llm",
        }

    def _rule_based_from_context(self, context: str, framework: str) -> Dict:
        return {
            "reasoning_confidence": 50,
            "executive_summary": f"Analysis of {framework} compliance shows gaps that require attention.",
            "gap_explanations": [],
            "improvement_suggestions": [],
            "rewritten_clauses": [],
            "cia_impact_summary": {},
            "source": "rule_based_fallback",
        }

    # ── Rule-based fallback ───────────────────────────────────────
    def _rule_based_reasoning(
        self, structural_missing, semantic_weak, missing_controls,
        structural_results, semantic_results, cia_analysis, framework,
    ) -> Dict:
        struct_score = structural_results.get("structural_score", 0)
        sem_score = semantic_results.get("semantic_score", 0)
        avg = (struct_score + sem_score) / 2

        # Executive summary
        if avg >= 80:
            exec_summary = (
                f"The document demonstrates strong alignment with {framework.upper()} requirements. "
                f"Structural compliance is at {struct_score}% with semantic similarity at {sem_score}%. "
                "Minor gaps should be addressed to achieve full compliance."
            )
        elif avg >= 50:
            exec_summary = (
                f"The document shows moderate compliance with {framework.upper()}. "
                f"Structural score is {struct_score}% and semantic score is {sem_score}%. "
                "Several mandatory sections require strengthening or addition."
            )
        else:
            exec_summary = (
                f"Significant gaps detected in {framework.upper()} compliance. "
                f"Structural coverage is only {struct_score}% with semantic alignment at {sem_score}%. "
                "Comprehensive remediation is required before audit readiness."
            )

        # Gap explanations with CIA impact
        gap_explanations = []
        for s in structural_missing[:6]:
            pillar = s.get("cia_pillar")
            cia_note = ""
            if pillar:
                cia_note = f" This weakens the **{pillar.title()}** pillar of the CIA triad."
            gap_explanations.append({
                "clause": s["clause"],
                "title": s["title"],
                "status": s["status"],
                "explanation": (
                    f"Clause {s['clause']} ({s['title']}) is {s['status']}. "
                    f"Keyword coverage is only {s.get('keyword_coverage', 0)}%.{cia_note}"
                ),
                "cia_impact": pillar,
            })

        # Improvement suggestions
        improvements = []
        if structural_results.get("missing", 0) > 0:
            missing_titles = [s["title"] for s in structural_missing if s["status"] == "missing"][:3]
            improvements.append(
                f"Add dedicated sections for: {', '.join(missing_titles)}"
            )
        if semantic_results.get("weak_count", 0) > 3:
            improvements.append(
                "Rewrite weak policy statements using mandatory language "
                "(shall, must, will) instead of vague terms (may, should consider)."
            )
        if missing_controls:
            mc_ids = [mc["control_id"] for mc in missing_controls[:3]]
            improvements.append(
                f"Address missing controls: {', '.join(mc_ids)}"
            )

        # CIA impact from structural flags
        cia_flags = structural_results.get("cia_structural_flags", {})
        cia_impact = {}
        for pillar in ("confidentiality", "integrity", "availability"):
            flags = cia_flags.get(pillar, [])
            if flags:
                cia_impact[pillar] = {
                    "status": "at_risk",
                    "missing_clauses": [f["clause"] for f in flags],
                    "impact": f"Absence of {len(flags)} section(s) weakens {pillar.title()} pillar.",
                }
            else:
                cia_impact[pillar] = {"status": "covered", "missing_clauses": [], "impact": ""}

        if cia_analysis:
            cov = cia_analysis.get("cia_coverage", {})
            for pillar in ("confidentiality", "integrity", "availability"):
                val = cov.get(pillar, 0)
                if val < 25:
                    if pillar not in cia_impact or cia_impact[pillar]["status"] != "at_risk":
                        cia_impact[pillar] = {
                            "status": "at_risk",
                            "missing_clauses": [],
                            "impact": f"{pillar.title()} coverage is critically low at {val:.1f}%.",
                        }

        # Rewritten clauses (top weak semantic matches)
        rewritten = []
        for wc in semantic_weak[:2]:
            original = wc.get("clause_text", "")
            rewritten.append({
                "original": original,
                "improved": self._rewrite_clause(original),
                "matched_control": wc.get("best_control_id", ""),
            })

        # Reasoning confidence
        reasoning_conf = self._calc_confidence(struct_score, sem_score, len(gap_explanations))

        return {
            "reasoning_confidence": reasoning_conf,
            "executive_summary": exec_summary,
            "gap_explanations": gap_explanations,
            "improvement_suggestions": improvements,
            "rewritten_clauses": rewritten,
            "cia_impact_summary": cia_impact,
            "source": "rule_based",
        }

    # ── Helpers ────────────────────────────────────────────────────
    @staticmethod
    def _rewrite_clause(original: str) -> str:
        """Simple rule-based clause strengthening."""
        text = original
        replacements = {
            "should": "shall",
            "may": "must",
            "could": "shall",
            "might": "must",
            "where possible": "as a mandatory requirement",
            "if feasible": "as a requirement",
            "efforts will be made": "the organization shall ensure",
            "should consider": "shall implement",
        }
        for weak, strong in replacements.items():
            text = text.replace(weak, strong)
        if not text.endswith("."):
            text += "."
        return text

    @staticmethod
    def _calc_confidence(struct_score: float, sem_score: float, n_gaps: int) -> float:
        """Heuristic confidence based on coverage and gaps."""
        base = (struct_score * 0.4 + sem_score * 0.4)
        penalty = min(n_gaps * 3, 30)
        return round(max(0, min(100, base + 20 - penalty)), 2)


# ── Singleton ─────────────────────────────────────────────────────
reasoning_engine = ReasoningEngine()
