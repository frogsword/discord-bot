import cred
import discord
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

PATH = Service(executable_path=cred.DRIVER_PATH)


def get_ub_build(champion_name):
    driver = webdriver.Chrome(executable_path=cred.DRIVER_PATH)
    driver.get("https://ultimate-bravery.net")
    driver.implicitly_wait(15)
    select_btn = driver.find_element(By.ID, 'champSelectionBtn')
    select_btn.click()
    deselect_btn = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[4]/div[1]/div/div/button[2]')
    deselect_btn.click()

    filter_input = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[4]/div[1]/input')
    filter_input.click()
    filter_input.send_keys(champion_name)

    champion = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[4]/div[2]/div')
    champion.click()

    lets_go_btn = driver.find_element(By.ID, 'braveryBtn')
    lets_go_btn.click()
    driver.implicitly_wait(15)

    build = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[1]')
    build.screenshot('build.png')

    driver.quit()

    return open('build.png', mode='r')


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('/'):
            champion_name = message.content.split('/')[1]
            await message.channel.send("Searching for best possible build...")
            try:
                get_ub_build(champion_name=champion_name)
                await message.channel.send(file=discord.File("build.png"))

            except:
                await message.channel.send("Invalid champion name!")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(cred.DISCORD_BOT_TOKEN)
