defmodule QuotationTest do
  use ExUnit.Case
  doctest Quotation

  test "greets the world" do
    assert Quotation.hello() == :world
  end
end
