import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json") as players_file:
        players_info = json.load(players_file)

    for nickname, player in players_info.items():

        race_info = player.get("race", {})
        race_name = race_info.get("name")
        race_description = race_info.get("description")

        guild = player.get("guild")
        if guild:
            guild_name = guild.get("name")
            guild_description = guild.get("description")
            guild, created = Guild.objects.get_or_create(
                name=guild_name, defaults={"description": guild_description}
            )

        race, created = Race.objects.get_or_create(
            name=race_name, defaults={"description": race_description}
        )

        skills = race_info.get("skills", [])
        for skill in skills:
            skill_name = skill.get("name")
            skill_bonus = skill.get("bonus")
            Skill.objects.get_or_create(
                name=skill_name, race=race, defaults={"bonus": skill_bonus}
            )

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": player.get("email"),
                "bio": player.get("bio"),
                "race": race,
                "guild": guild,
            },
        )


if __name__ == "__main__":
    main()
