import re
from discord import File

from . import messages

class AbstractCommand(object):
    """Base class for commands"""

    def __init__(self, message):
        super(AbstractCommand, self).__init__()
        self.message = message

    async def execute(self, client):
        raise Exception(f'Execute not implemented for {self}')

class HelpCommand(AbstractCommand):
    """Responds with a message with bot usage info and commands"""

    _name = "help"
    _description = "Display bot usage and help"
    _example_arguments = None

    def __init__(self, message, args):
        super(HelpCommand, self).__init__(message)

    async def execute(self, client):
        await self.message.channel.send(
            embed=messages.help_message(client.get_commands())
        )

class InfoCommand(AbstractCommand):
    """Responds with a message with bot information"""

    _name = "info"
    _description = "Display bot info"
    _example_arguments = None

    def __init__(self, message, args):
        super(InfoCommand, self).__init__(message)

    async def execute(self, client):
        await self.message.channel.send(embed=messages.INFO)


class AddSkillCommand(AbstractCommand):
    """Creates a new skill in the graph"""

    _name = "new"
    _description = "Create a new skill"
    _example_arguments = ["fishing", "dancing"]
    _skill_re = re.compile('^[\w][\w_]+$')

    def __init__(self, message, args):
        super(AddSkillCommand, self).__init__(message)
        print(f'🐛 Args: {args}')
        if not args:
            raise Exception("Missing skill name :shrug:")
        skill_name = re.sub(r'\W+', '_', args)
        print(f'🐛 skill_name: {skill_name}')
        if not AddSkillCommand._skill_re.match(skill_name):
            raise Exception("Invalid skill name :shrug:")
        self.skill_name = skill_name.lower()

    async def execute(self, client):
         m = await self.message.channel.send(
            embed=messages.new_skill_message(self.skill_name)
         )
         await m.add_reaction("✅")
         client.create_skill(m.id, self.skill_name)

class DrawFullGraphCommand(AbstractCommand):
    """Creates an image of the whole graph"""

    _name = "fullgraph"
    _description = "Draw the full graph"
    _example_arguments = None

    def __init__(self, message, args):
        super(DrawFullGraphCommand, self).__init__(message)

    async def execute(self, client):
        from render import PNGRenderer
        png_file = PNGRenderer(client.get_graph_snapshot()).render()

        m = await self.message.channel.send(
            embed=messages.FULL_GRAPH,
            file=File(png_file)
        )
