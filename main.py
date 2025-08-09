import json

import init_django_orm  # noqa: F401

from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json") as players_file:
        players_info = json.load(players_file)

    for nickname, player in players_info.items():

        race_name = player.get("race").get("name")
        race_description = (
            player.get("race").get("description")
            if player.get("race").get("description")
            else None
        )

        guild = player.get("guild")
        if guild:
            guild_name = guild.get("name")
            guild_description = (
                guild.get("description") if guild.get("description") else None
            )
            guild, created = Guild.objects.get_or_create(
                name=guild_name, defaults={"description": guild_description}
            )

        race, created = Race.objects.get_or_create(
            name=race_name, defaults={"description": race_description}
        )

        for skill in player.get("race").get("skills"):
            skill_name = skill.get("name")
            skill_bonus = skill.get("bonus")
            Skill.objects.get_or_create(
                name=skill_name, race=race, defaults={"bonus": skill_bonus}
            )

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": player["email"],
                "bio": player["bio"],
                "race": race,
                "guild": guild,
            },
        )


if __name__ == "__main__":
    main()
