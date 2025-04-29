from db import get_session
from models.team_member import TeamMember

def fetch_team_members():
    try:
        with get_session() as session:
            members = session.query(TeamMember).all()

            response = [
                {
                    "name": m.name,
                    "position": m.role,
                    "description": m.bio,
                    "image": m.photo_url  # Match what React expects
                }
                for m in members
            ]

            return response

    except Exception as e:
        # Return a plain dictionary instead of a Flask Response
        return {"error": f"An error occurred: {str(e)}"}
