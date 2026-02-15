"""ATS resume optimization service (multi-provider friendly)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal

ATSProvider = Literal[
    "workday",
    "greenhouse",
    "lever",
    "taleo",
    "icims",
    "sap_successfactors",
    "smartrecruiters",
    "bamboohr",
    "generic",
]

SUPPORTED_ATS: list[ATSProvider] = [
    "workday",
    "greenhouse",
    "lever",
    "taleo",
    "icims",
    "sap_successfactors",
    "smartrecruiters",
    "bamboohr",
    "generic",
]


@dataclass
class ATSOptimizationResult:
    provider: ATSProvider
    score: int
    missing_keywords: List[str]
    suggestions: List[str]
    optimized_text: str


class ResumeOptimizer:
    provider_focus = {
        "workday": ["experience", "skills", "education", "leadership"],
        "greenhouse": ["impact", "metrics", "ownership", "stack"],
        "lever": ["results", "collaboration", "delivery", "product"],
        "taleo": ["keywords", "compliance", "certification", "tenure"],
        "icims": ["skills", "domain", "projects", "achievements"],
        "sap_successfactors": ["enterprise", "process", "governance", "kpi"],
        "smartrecruiters": ["outcomes", "scalability", "innovation", "communication"],
        "bamboohr": ["culture", "team", "growth", "impact"],
        "generic": ["experience", "skills", "results", "projects"],
    }

    def optimize(self, resume_text: str, job_description: str, provider: ATSProvider = "generic") -> ATSOptimizationResult:
        provider = provider if provider in SUPPORTED_ATS else "generic"
        resume_norm = resume_text.lower()
        jd_norm = job_description.lower()

        keywords = self._extract_keywords(jd_norm)
        missing = [kw for kw in keywords if kw not in resume_norm][:12]

        focus = self.provider_focus.get(provider, self.provider_focus["generic"])
        focus_hits = sum(1 for token in focus if token in resume_norm)
        keyword_hits = max(0, len(keywords) - len(missing))
        score = min(100, int((keyword_hits * 7) + (focus_hits * 8) + 20))

        suggestions = [
            f"Adicionar termos críticos: {', '.join(missing[:6])}" if missing else "Cobertura de palavras-chave boa",
            "Incluir resultados mensuráveis (ex.: +25% conversão, -30% custo)",
            f"Ajustar seção de competências para padrões de {provider}",
            "Usar verbos de ação e bullets curtos (1-2 linhas)",
        ]

        optimized = self._build_optimized_resume(resume_text, missing, provider)

        return ATSOptimizationResult(
            provider=provider,
            score=score,
            missing_keywords=missing,
            suggestions=suggestions,
            optimized_text=optimized,
        )

    def _extract_keywords(self, jd_text: str) -> List[str]:
        base = [
            "python", "fastapi", "aws", "docker", "kubernetes", "sql", "postgresql",
            "redis", "api", "security", "monitoring", "leadership", "communication",
        ]
        dynamic = [w.strip(".,:;()[]{}") for w in jd_text.split() if len(w) > 4]
        dedup = []
        for token in base + dynamic:
            if token not in dedup and token.isascii():
                dedup.append(token)
        return dedup[:24]

    def _build_optimized_resume(self, original: str, missing: List[str], provider: str) -> str:
        appendix = "\n".join([f"- {kw}" for kw in missing[:10]]) if missing else "- Nenhuma keyword crítica ausente"
        return (
            f"{original.strip()}\n\n"
            f"--- ATS OPTIMIZATION ({provider.upper()}) ---\n"
            "Sugestões aplicadas:\n"
            "- Estrutura orientada a resultados\n"
            "- Palavras-chave alinhadas com vaga\n"
            "- Terminologia compatível com ATS\n\n"
            "Keywords recomendadas:\n"
            f"{appendix}\n"
        )


def generate_resume_pdf(content: str) -> bytes:
    """Generate simple PDF bytes without external dependencies."""
    safe = content.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    lines = [safe[i:i + 90] for i in range(0, len(safe), 90)] or ["Resume optimized"]

    text_lines = "\n".join([f"({ln}) Tj" for ln in lines[:80]])
    stream = f"BT /F1 10 Tf 40 800 Td 0 -14 Td {text_lines} ET"

    objects = [
        "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj",
        "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj",
        "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj",
        "4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj",
        f"5 0 obj << /Length {len(stream)} >> stream\n{stream}\nendstream endobj",
    ]

    pdf = "%PDF-1.4\n"
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf.encode("latin-1")))
        pdf += obj + "\n"

    xref_pos = len(pdf.encode("latin-1"))
    pdf += f"xref\n0 {len(offsets)}\n"
    pdf += "0000000000 65535 f \n"
    for off in offsets[1:]:
        pdf += f"{off:010d} 00000 n \n"
    pdf += f"trailer << /Root 1 0 R /Size {len(offsets)} >>\nstartxref\n{xref_pos}\n%%EOF"

    return pdf.encode("latin-1", errors="ignore")
