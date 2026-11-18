import os
import signal
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface

# Carrega as variáveis do arquivo .env
load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

if not API_KEY or not AGENT_ID:
    raise ValueError("Verifique se ELEVENLABS_API_KEY e AGENT_ID estão no arquivo .env")

def main():
    client = ElevenLabs(api_key=API_KEY)

    # Inicializa a conversa conectando o microfone padrão
    conversation = Conversation(
        client=client,
        agent_id=AGENT_ID,
        requires_auth=True,
        audio_interface=DefaultAudioInterface(),
        # Callbacks para acompanhar o texto no terminal
        callback_agent_response=lambda response: print(f"\n🤖 TurIA: {response}"),
        callback_user_transcript=lambda transcript: print(f"🎙️ Você: {transcript}"),
    )

    # Permite encerrar o programa limpamente com Ctrl+C
    signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

    print("Iniciando conexão com a TurIA... (Pressione Ctrl+C para sair)")
    conversation.start_session()
    
    # Mantém o script rodando enquanto a conversa estiver ativa
    conversation.wait_for_session_end()
    print("\nSessão encerrada.")

if __name__ == "__main__":
    main()