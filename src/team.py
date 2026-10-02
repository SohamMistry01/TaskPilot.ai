# src/team.py

"""
Default team configuration for TaskPilot AI.

For the MVP, team members are hardcoded rather than stored in a database.
"""

from src.models import TeamMember


TEAM_MEMBERS = [
    TeamMember(
        name="Rahul",
        role="Frontend Developer",
        skills=[
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "UI implementation",
        ],
    ),
    TeamMember(
        name="Priya",
        role="Backend Developer",
        skills=[
            "Python",
            "Django",
            "FastAPI",
            "REST APIs",
            "PostgreSQL",
        ],
    ),
    TeamMember(
        name="Amit",
        role="UI/UX Designer",
        skills=[
            "Figma",
            "UI Design",
            "UX Design",
            "Wireframing",
            "Prototyping",
        ],
    ),
    TeamMember(
        name="Neha",
        role="QA Engineer",
        skills=[
            "Software Testing",
            "API Testing",
            "Test Automation",
            "Bug Detection",
            "Quality Assurance",
        ],
    ),
]


def get_team_members() -> list[TeamMember]:
    """
    Return the available team members.
    """

    return TEAM_MEMBERS