from dataclasses import dataclass
from environs import Env


@dataclass
class Bot:
    token: str


@dataclass
class Mail:
    mail_user: str
    mail_password: str
    to_email: str

@dataclass
class NatsConf:
    token: str

@dataclass
class Config:
    bot: Bot
    mail: Mail
    nats: NatsConf

def load_config():
    env = Env()
    env.read_env()
    return Config(
        bot=Bot(
            token=env('BOT_TOKEN')
        ),
        mail=Mail(
            mail_user=env('MAIL_USER'),
            mail_password=env('MAIL_PASSWORD'),
            to_email=env('TO_EMAIL')
        ),
        nats=NatsConf(
            token=env('NATS_SERVER')
        )
    )
