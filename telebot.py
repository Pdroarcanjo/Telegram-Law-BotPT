import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Carregar variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
FOREFRONT_API_KEY = os.getenv("FOREFRONT_API_KEY")

# Verificar se os tokens estão configurados
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("ERRO: O token do Telegram não foi configurado corretamente.")
if not FOREFRONT_API_KEY:
    raise ValueError("ERRO: O token da Forefront AI não foi configurado corretamente.")

# URL da API da Forefront AI
FOREFRONT_API_URL = "https://api.forefront.ai/v1/chat/completions"

# Função para chamar a API da Forefront AI
def consultar_ia(mensagem):
    headers = {
        "Authorization": f"Bearer {FOREFRONT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4",  # Ajuste o modelo conforme necessário
        "messages": [{"role": "user", "content": mensagem}],
        "temperature": 0.7
    }

    response = requests.post(FOREFRONT_API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Erro ao consultar a IA: {response.status_code} - {response.json()}"

# Comando /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Olá! Eu sou um bot com Forefront AI. Envie uma mensagem e eu responderei!")

# Função principal para processar mensagens
async def responder(update: Update, context: CallbackContext):
    user_message = update.message.text
    resposta_ia = consultar_ia(user_message)
    await update.message.reply_text(resposta_ia)

# Configuração do bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot está rodando...")
    app.run_polling()

# Iniciar o bot
if __name__ == "__main__":
    main()

