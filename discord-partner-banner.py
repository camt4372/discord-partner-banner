import discord

intents = discord.Intents.default()
intents.members = True
intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!배너생성'):
        author_id = 839827018396336128  # 명령어를 사용할 수 있는 사람 아이디
        user_role_id = 1104118426278039644  # 유저 역할 아이디 (없으면 암거나)

        if message.author.id == author_id:
            guild = message.guild

            command_args = message.content.split()
            if len(command_args) < 3:
                await message.channel.send('배너명과 멘션을 똑바로 입력해주세요.')
                return

            배너명 = command_args[1]
            멘션 = command_args[2]

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(send_messages=False, read_message_history=True),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                guild.get_role(user_role_id): discord.PermissionOverwrite(read_messages=True, send_messages=False, mention_everyone=True),
                message.mentions[0]: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }

            category_id = 1106782722032156762  # 이미 만들어진 카테고리 아이디(거기에 채널추가됨)
            existing_category = guild.get_channel(category_id)

            if existing_category is None or not isinstance(existing_category, discord.CategoryChannel):
                await message.channel.send('카테고리를 찾을 수 없습니다.')
                return

            channel = await existing_category.create_text_channel(f'『🤝』：{배너명}', overwrites=overwrites) # 『🤝』：{배너명}에서 『🤝』：만 바꿔서 사용가능 '📢ㅣ{배너명}' 이런것 처럼

            reply_embed = discord.Embed(
                title='배너가 생성되었습니다.',
                description=f'배너가 생성되었습니다.\n배너가기: {channel.mention}',
                color=0x00FF00
            )

            await message.reply(embed=reply_embed)

            mention_message = f'{멘션}'
            await channel.send(mention_message)
        else:
            embed = discord.Embed(
                title='오류',
                description='이 명령어를 사용할 권한이 없습니다.',
                color=0xFF0000
            )
            await message.channel.send(embed=embed)

client.run('') # 봇 토큰 넣어요.
