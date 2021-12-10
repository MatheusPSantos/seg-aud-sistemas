defmodule Atividade3.Crypto do

  #especifica os campos para serem
  # hasheados num bloco
  @hash_fields [:data, :timestamp, :hash_anterior]

  # define a função de sha256
  defp sha256(binary) do
    :crypto.hash(:sha256, binary)
    |> Base.encode16
  end
  # calcula o hash do bloco
  def hash(%{} = block) do
    block
    |> Map.take(@hash_fields)
    |> Poison.encode!
    |> sha256
  end

  # calcula e adiciona o hash no bloco
  def add_hash(%{} = block) do
    %{ block | hash: hash(block) }
  end
end
