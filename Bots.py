import os
import asyncio
import discord
from discord.ext import commands
from keep_alive import keep_alive

# Configuration des Intentions (Intents)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot connecté en tant que {bot.user.name} ({bot.user.id})")
    print("--------------------------------------------------")

# 🔄 Commande pour synchroniser instantanément les commandes Slash
@bot.command(name="sync")
@commands.has_permissions(administrator=True)
async def sync_commands(ctx):
    msg = await ctx.send("🔄 Synchronisation forcée sur ce serveur...")
    try:
        bot.tree.copy_global_to(guild=ctx.guild)
        synced = await bot.tree.sync(guild=ctx.guild)
        await msg.edit(content=f"✅ **{len(synced)}** commandes Slash chargées sur ce serveur !")
    except Exception as e:
        await msg.edit(content=f"❌ Erreur de synchronisation : `{e}`")

# 📂 Chargement automatique de tous les cogs (Cogs et Tickets)
async def load_extensions():
    # 1. Dossier Cogs
    if os.path.exists("./Cogs"):
        for filename in os.listdir("./Cogs"):
            if filename.endswith(".py") and not filename.startswith("__"):
                try:
                    await bot.load_extension(f"Cogs.{filename[:-3]}")
                    print(f"✅ Cog Cogs.{filename[:-3]} chargé")
                except Exception as e:
                    print(f"❌ Erreur lors du chargement de Cogs.{filename[:-3]} : {e}")

    # 2. Dossier Tickets
    if os.path.exists("./Tickets"):
        for filename in os.listdir("./Tickets"):
            if filename.endswith(".py") and not filename.startswith("__"):
                try:
                    await bot.load_extension(f"Tickets.{filename[:-3]}")
                    print(f"✅ Cog Tickets.{filename[:-3]} chargé")
                except Exception as e:
                    print(f"❌ Erreur lors du chargement de Tickets.{filename[:-3]} : {e}")

async def main():
    # Lancement du serveur Web de maintien en vie sur Render
    if os.getenv("RENDER"):
        keep_alive()

    # Récupération du TOKEN depuis les variables de Render
    token = os.getenv("TOKEN")
    
    if not token:
        # Fichier local de secours si tu testes sur ton PC
        try:
            from Token import TOKEN as local_token
            token = local_token
        except ImportError:
            print("❌ Aucun TOKEN trouvé ! Ajoute la variable 'TOKEN' sur Render.")
            return

    async with bot:
        await load_extensions()
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
