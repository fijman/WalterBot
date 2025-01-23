
import discord
from discord.ext import commands
import settings
# Указываем необходимые намерения
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Необходимо для получения содержимого сообщений

# Создаем экземпляр бота
bot = commands.Bot(command_prefix='!', intents=intents)

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Взять дело", style=discord.ButtonStyle.primary)
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        # Используем interaction.edit_original_message для редактирования исходного сообщения
        embed = interaction.message.embeds[0]  # Получаем оригинальный embed
        embed.color = discord.Color.green()  # Меняем цвет на зеленый

        # Удаляем кнопку, редактируя сообщение
        await interaction.response.edit_message(
            content=f"**Дело взял: {interaction.user.mention}!**",
            embed=embed,  # Отправляем обновленный embed
            view=None  # Удаляем кнопки
        )
        
        

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_message(message):
    # Проверяем, что сообщение пришло от вебхука и не от самого бота
 
    if message.channel.id == settings.CHANNEL_ID and message.webhook_id and message.author.bot:
        # Создаем embed с содержимым оригинального сообщения
        embeds = discord.Embed(
            title=message.embeds[0].title if message.embeds else "Сообщение",
            description= '<@1321467897834639411>',
            color=discord.Color.from_rgb(78, 80, 88)
        )

        # Копируем поля из оригинального embed, если они есть
        if message.embeds:
            for field in message.embeds[0].fields:
                embeds.add_field(name=field.name, value=f"> {field.value}", inline=field.inline)

            # Копируем footer, если он есть
            if message.embeds[0].footer:
                embeds.set_footer(text=message.embeds[0].footer.text)

            # Копируем thumbnail, если он есть
            if message.embeds[0].thumbnail:
                embeds.set_thumbnail(url=message.embeds[0].thumbnail.url)

            # Копируем image, если он есть
            if message.embeds[0].image:
                embeds.set_image(url=message.embeds[0].image.url)

        # Получаем канал по ID и отправляем новое сообщение с кнопкой и embed
        channel = bot.get_channel(settings.CHANNEL_ID)
        if channel:
            sent_message = await channel.send(embed=embeds, view=MyView())

        # Удаляем оригинальное сообщение
        await message.delete()
        
if __name__ == "__main__":
  # Запуск бота
  bot.run(settings.TOKEN)