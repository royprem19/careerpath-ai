from backend.models.schemas import GapAnalysisResponse
from backend.services.ml_engine import salary_predictor, analyze_skill_market_velocity

def compute_gap(
    user_skills: list[str], 
    role_essential_skills: list[str], 
    role_optional_skills: list[str], 
    role_title: str = "",
    role_category: str = "",
    years_exp: float = 0.0
) -> GapAnalysisResponse:
    user_skills_lower = {s.strip().lower() for s in user_skills if s.strip()}
    
    essential_dict = {s.strip().lower(): s.strip() for s in role_essential_skills if s.strip()}
    optional_dict = {s.strip().lower(): s.strip() for s in role_optional_skills if s.strip()}
    
    matched_essential = [essential_dict[s] for s in essential_dict if s in user_skills_lower]
    matched_optional = [optional_dict[s] for s in optional_dict if s in user_skills_lower]
    
    missing_essential = [essential_dict[s] for s in essential_dict if s not in user_skills_lower]
    missing_optional = [optional_dict[s] for s in optional_dict if s not in user_skills_lower]
    
    all_role_skills_lower = set(essential_dict.keys()).union(set(optional_dict.keys()))
    surplus_skills = [s for s in user_skills if s.strip().lower() not in all_role_skills_lower]
    
    matched_skills = matched_essential + matched_optional
    
    essential_cov = (len(matched_essential) / len(role_essential_skills)) if role_essential_skills else 1.0
    optional_cov = (len(matched_optional) / len(role_optional_skills)) if role_optional_skills else 1.0
    
    # 70% essential + 30% optional coverage
    fit_score = round(((0.7 * essential_cov) + (0.3 * optional_cov)) * 100, 1)
    essential_coverage_pct = round(essential_cov * 100, 1)
    optional_coverage_pct = round(optional_cov * 100, 1)
    
    total_req = len(role_essential_skills) + len(role_optional_skills)
    matched_cnt = len(matched_skills)
    
    # ML Salary Prediction
    is_ai_or_cloud = "AI" in role_category or "Cloud" in role_category or "Data Science" in role_category
    comp_pred = salary_predictor.predict_compensation(
        num_skills=len(user_skills),
        years_exp=years_exp,
        essential_ratio=essential_cov,
        is_ai_or_cloud=is_ai_or_cloud
    )
    
    # Market demand velocities for missing essential skills
    missing_velocities = analyze_skill_market_velocity(missing_essential[:6])
    
    is_exploratory = fit_score < 35.0
    if is_exploratory:
        conf_level = "Exploratory"
    elif fit_score < 60.0:
        conf_level = "Moderate"
    else:
        conf_level = "High"

    # Generate explainable narrative
    if is_exploratory:
        why_str = (
            f"Career Discovery Mode: Current alignment is {fit_score}%. Rather than jumping directly to specialized roles, "
            f"we recommend building core competencies in {', '.join(role_essential_skills[:3])} through our accredited foundational roadmap."
        )
    elif matched_essential:
        matched_preview = ", ".join(matched_essential[:4])
        why_str = (
            f"You match key essential requirements including {matched_preview}. "
            f"Our ML salary model benchmarks your profile around {comp_pred['salary_range']} in the Indian market. "
            f"Bridging the {len(missing_essential)} core missing competencies will unlock the top quartile compensation."
        )
    else:
        why_str = (
            f"This role requires building foundational skills in {', '.join(role_essential_skills[:3])}. "
            f"Expected fresher/entry band: {comp_pred['salary_range']}. "
            f"Following our roadmap will elevate your profile step-by-step."
        )
        
    return GapAnalysisResponse(
        fit_score=fit_score,
        essential_coverage=essential_coverage_pct,
        optional_coverage=optional_coverage_pct,
        missing_essential=missing_essential,
        missing_optional=missing_optional,
        matched_skills=matched_skills,
        surplus_skills=surplus_skills,
        total_required=total_req,
        matched_count=matched_cnt,
        why_this_role=why_str,
        predicted_salary=comp_pred["salary_range"],
        skill_velocities=missing_velocities,
        confidence_level=conf_level,
        is_exploratory_mode=is_exploratory,
        disclaimer="Estimated market compensation reflects median hiring data for candidates clearing technical rounds and is not a guaranteed job offer."
    )
