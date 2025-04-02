# from taskiq import TaskiqScheduler
# from taskiq_nats import PullBasedJetStreamBroker, NATSObjectStoreResultBackend, NATSKeyValueScheduleSource
#
# import bot.config as config
#
# config = config.load_config()
#
# worker = PullBasedJetStreamBroker(
#     servers=config.nats.token,
#     queue='taskiq_queue').with_result_backend(
#     result_backend=NATSObjectStoreResultBackend(servers=config.nats.token)
# )
#
# scheduler_storage = NATSKeyValueScheduleSource(servers=config.nats.token)
# scheduler = TaskiqScheduler(worker, sources=[scheduler_storage])
