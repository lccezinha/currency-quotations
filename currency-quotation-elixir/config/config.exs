use Mix.Config

config :kaffe,
  consumer: [
    endpoints: [localhost: 9092],
    # the topic(s) that will be consumed
    topics: ["quotation_topic_awesome_api", "quotation_topic_rate_api"],
    # the consumer group for tracking offsets in Kafka
    consumer_group: "quotation_consumer_group",
    # the module that will process messages
    message_handler: Quotation.Consumer
  ]
