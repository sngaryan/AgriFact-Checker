import pytest
from services.topic_checker import check_agricultural_relevance
from app import app

def test_video_game_text_out_of_domain():
    """Verify that video game challenge text (from user's screenshot) is identified as not relevant to agriculture."""
    game_text = (
        "Drop a healing or shielding item and ping it for squad members in 3 different matches. "
        "Craft 5 times at a Replicator in Unranked BR Trios/Duos. "
        "As an Assault Legend open the Extra Compartment on 3 different Weapon Supply Bins. "
        "Open 3 Extended Supply Bins as a Support Legend. "
        "Use a Survey Beacon as a Recon Legend 3 times. "
        "Get 3 kills or assists. Evolve armor to epic tier 3 times."
    )
    res = check_agricultural_relevance(game_text)
    assert res["is_relevant"] is False
    assert len(res["matched_terms"]) == 0

def test_legitimate_agri_text_relevant():
    """Verify that agricultural claims and scheme forwards are correctly marked as relevant."""
    agri_text = "Farmers can register for PM-Kisan scheme on official portal to receive Rs 6000 annual subsidy support for crop cultivation."
    res = check_agricultural_relevance(agri_text)
    assert res["is_relevant"] is True
    assert "kisan" in res["matched_terms"] or "crop" in res["matched_terms"] or "subsidy" in res["matched_terms"]

def test_hindi_agri_text_relevant():
    """Verify that Hindi agricultural text is correctly marked as relevant."""
    hindi_text = "किसान क्रेडिट कार्ड (KCC) योजना के तहत किसानों को फसल बुवाई के लिए कम ब्याज दर पर लोन मिलता है।"
    res = check_agricultural_relevance(hindi_text)
    assert res["is_relevant"] is True

def test_app_check_endpoint_out_of_domain():
    """Integration test verifying POST /check classifies non-agri video game text as out_of_domain."""
    with app.test_client() as client:
        response = client.post("/check", data={
            "text": "Craft 5 times at a Replicator in Unranked BR. Open 3 Extended Supply Bins as Support Legend."
        })
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Non-Agricultural Content" in html or "out_of_domain" in html
