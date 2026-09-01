from phoenix_core.experiment_specialist import design_experiment
from phoenix_core.opportunity_specialist import discover_opportunity
from phoenix_core.intelligence_specialist import synthesize_intelligence
from phoenix_core.specialist_router import route_specialists, specialist_registry


def test_experiment_plan():
    plan = design_experiment(
        hypothesis="نتیجه‌محور بودن CTA نرخ تبدیل را افزایش می‌دهد",
        variant_a="CTA فعلی",
        variant_b="CTA نتیجه‌محور",
        primary_kpi="conversion_rate",
    )
    assert plan.variant_a and plan.variant_b
    assert plan.primary_kpi == "conversion_rate"
    assert plan.guardrail_kpis


def test_opportunity_requires_evidence():
    item = discover_opportunity(
        signal="افزایش ذخیره محتوا",
        opportunity="تبدیل موضوع به سری محتوایی",
        evidence=["save_rate افزایش یافته"],
        value_hypothesis="افزایش بازگشت مخاطب",
        recommended_action="اجرای تست سه قسمتی",
        risk="اشباع موضوع",
    )
    assert item.human_approval_required is True


def test_intelligence_brief():
    brief = synthesize_intelligence(
        question="فرصت بازار چیست؟",
        signals=["رشد تقاضا"],
        patterns=["افزایش جست‌وجو"],
        implications=["فرصت ورود"],
        recommended_next_step="اعتبارسنجی بازار",
        confidence=0.8,
    )
    assert brief.confidence == 0.8
    assert brief.human_approval_required is True


def test_router_has_15_specialists_and_routes_new_domains():
    registry = specialist_registry()
    assert len(registry) == 15
    routed = route_specialists(problem="بازار رقبا و فرصت پنهان را بررسی و یک آزمایش برای افزایش تبدیل طراحی کن")
    keys = {item["key"] for item in routed}
    assert keys & {"experiment", "opportunity", "intelligence"}
    assert all(item["human_approval_required"] for item in routed)
