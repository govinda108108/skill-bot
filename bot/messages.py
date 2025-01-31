from collections.abc import Iterable

import discord
from constants import Strings as k

COLOR = discord.Colour.magenta()

HELLO = discord.Embed(
    title = k.HELLO_TITLE,
    colour = COLOR,
    description = k.DESCRIPTION + f'''

        Try `{k.COMMAND_PREFIX} help` to learn more.
    '''
)

INFO = discord.Embed(
    title = "ℹ️\nInfo!",
    colour = COLOR,
    description = k.INFO_MESSAGE
)

FULL_GRAPH = discord.Embed(
    title = "☝️\nHere's your map!",
    colour = COLOR,
    description = f'It includes *all* {k.PEOPLE} and all {k.ENTITIES_LONG}'
)

WORD_CLOUD_GRAPH = discord.Embed(
    title = "☝️\nHere's your words cloud!",
    colour = COLOR,
    description = f'Words size is proportional to {k.WORD_CLOUD_SIZE}'
)

def command_error_message(command, e):
    return discord.Embed(
        title = "🤦‍♂️\nOoops!",
        colour = COLOR,
        description = f'''
            Something went wrong with command: `{command}`

            {repr(e)}

            **If you think this is a bug**, give a shout to {k.ERROR_CONTACT_PERSON}
        '''
    )

def new_skill_message(skill_name):
    return discord.Embed(
        title = f'{k.SKILL_ICON} {skill_name} {k.SKILL_ICON}',
        colour = COLOR,
        description = f'''
            New {k.ENTITY_SHORT} created.

            **React with {k.REACTION} to this message if you {k.REACTION_REASON}**
        '''
    )

def duplicate_skill_message(skill_name: str, skill_id: int, guild_id: int, channel_id: int):
    return discord.Embed(
        title = f'Duplicate {skill_name}',
        colour = COLOR,
        description = f'''
            The {k.ENTITY_SHORT} already exists!

            You should react with {k.REACTION} to the original message:
            https://discord.com/channels/{guild_id}/{channel_id}/{skill_id}
        '''
    )

def help_message(commands):
    embed = discord.Embed(
        title = "❓\nHelp!",
        colour = COLOR,
        description = f'''
            Use these commands to create a new {k.ENTITY_SHORT}.
            Or visualize the current state of {k.ENTITIES_LONG} and {k.PEOPLE} connected to them.

            To associate yourself with a exsiting {k.ENTITY_SHORT}, reacting with {k.REACTION} to the corresponding bot message.
        '''
    )
    for c in commands:
        command_string = f'`{k.COMMAND_PREFIX} {c._name}`'
        description = c._description
        if c._example_arguments:
            for ex in c._example_arguments:
                description += f'\n*Example*: `{k.COMMAND_PREFIX} {c._name} {ex}`'
        embed.add_field(name=command_string, value=description)
    return embed

def list_message(guild_id: int, channel_id: int, skills: Iterable, num_pages: int, current_page: int):
    embed = discord.Embed(
        title = f'List of {k.ENTITIES_LONG} (page {current_page} / {num_pages})',
        colour = COLOR,
        description = f'''
            Click on the **show** link to jump to the {k.ENTITY_SHORT}
        '''
    )
    for skill in skills:
        name_link=f'{k.SKILL_ICON} {skill.name}'
        description=f'''
            {len(skill.people)} {k.PEOPLE}
            [show](https://discord.com/channels/{guild_id}/{channel_id}/{skill.id})
        '''
        embed.add_field(name=name_link, value=description)
    return embed

def paginated_list_messages(guild_id: int, channel_id: int, skills: Iterable, page_size: int = 25):
    paginated_skills = [skills[i:i + page_size] for i in range(0, len(skills), page_size)]
    num_pages = len(paginated_skills)
    return [list_message(guild_id, channel_id, paginated_skills[index], num_pages, index+1) for index in range(len(paginated_skills))]


def people_subgraph_message(people_ids: Iterable[int]):
    mentions = ", ".join(f'<@!{pid}>' for pid in people_ids)
    embed = discord.Embed(
        title = "☝️\nHere's your map!",
        colour = COLOR,
        description = f'''
            It includes only a subset of {k.PEOPLE}: {mentions}
            (and the {k.ENTITIES_LONG} linked to them)
        '''
    )
    return embed

def skills_subgraph_message(skills_terms: Iterable[str]):
    terms_string = ", ".join(f'"{term}"' for term in skills_terms)
    embed = discord.Embed(
        title = "☝️\nHere's your map!",
        colour = COLOR,
        description = f'''
            It includes only {k.ENTITY_SHORT} matching: {terms_string}
        '''
    )
    return embed

def stats_message(people_count: int, skills_count: int, people_skills_count: int):
    embed = discord.Embed(
        title = "📊\nStatistics",
        colour = COLOR,
        description = f'''
            👤 {k.PEOPLE_UPPERCASE}: {people_count}
            {k.SKILL_ICON} {k.ENTITIES_LONG_UPPERCASE}: {skills_count}
            ↔️ Connections: {people_skills_count}
        '''
    )
    return embed
