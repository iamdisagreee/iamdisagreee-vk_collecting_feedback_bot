from taskiq import TaskiqScheduler
from taskiq_nats import PullBasedJetStreamBroker, NATSObjectStoreResultBackend, NATSKeyValueScheduleSource

worker = PullBasedJetStreamBroker(
    servers='localhost',
    queue='taskiq_queue').with_result_backend(
    result_backend=NATSObjectStoreResultBackend(servers='localhost')
)

scheduler_storage = NATSKeyValueScheduleSource(servers="localhost")
scheduler = TaskiqScheduler(worker, sources=[scheduler_storage])
