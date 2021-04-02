defmodule Quotation.Consumer do
  def handle_message(%{topic: topic, value: value}) when not is_nil(value) when not is_nil(topic) do
    decoded = Poison.decode!(value)
    quotation = %Quotation{
      currency_from: decoded["currency_from"],
      currency_to: decoded["currency_to"],
      amount: decoded["amount"],
      quotation_value: decoded["quotation_value"],
      source: topic
    }
    IO.inspect(quotation)
    :ok
  end
end
